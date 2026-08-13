from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from src.detectors import (
    detect_person_names,
    detect_emails,
    detect_phone_numbers,
    detect_company_names,
    detect_ssns,
    detect_credit_cards,
    detect_dates_of_birth,
    detect_ip_addresses,
)

from src.document_reader import read_docx
from src.redactor import redact_docx


app = FastAPI(
    title="PII Detection and Redaction API",
    description=(
        "Detects personally identifiable information in DOCX documents "
        "and generates a redacted DOCX with realistic fake replacements."
    ),
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "PII Detection and Redaction API is running",
        "docs": "/docs",
    }


def detect_all(text: str) -> dict[str, list[str]]:
    """
    Run all PII detectors.
    """

    return {
        "PERSON": detect_person_names(text),
        "EMAIL": detect_emails(text),
        "PHONE": detect_phone_numbers(text),
        "COMPANY": detect_company_names(
            text,
            allowed_only=True,
        ),
        "SSN": detect_ssns(text),
        "CREDIT_CARD": detect_credit_cards(text),
        "DOB": detect_dates_of_birth(text),
        "IP_ADDRESS": detect_ip_addresses(text),
    }


@app.post("/detect")
async def detect_and_redact(
    file: UploadFile = File(...),
):
    """
    Upload a DOCX document.

    The endpoint:
      1. Reads the document.
      2. Detects PII.
      3. Generates fake replacements using Faker.
      4. Creates a redacted DOCX.
      5. Returns the redacted DOCX for download.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided.",
        )

    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are supported.",
        )

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="pii_redaction_"
        )
    )

    input_path = temp_dir / "input.docx"
    output_path = temp_dir / "redacted.docx"

    try:
        # Save uploaded document.
        with input_path.open("wb") as output_file:
            shutil.copyfileobj(
                file.file,
                output_file,
            )

        # Read document.
        text = read_docx(input_path)

        # Detect PII.
        detections = detect_all(text)

        total_detected = sum(
            len(values)
            for values in detections.values()
        )

        # Generate fake replacements and create redacted document.
        replacements = redact_docx(
            input_file=input_path,
            output_file=output_path,
            detections=detections,
        )

        if not output_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Redacted document was not generated.",
            )

        # Return the redacted DOCX.
        return FileResponse(
            path=output_path,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            filename="Redacted_" + file.filename,
            headers={
                "X-PII-Total-Detected": str(
                    total_detected
                ),
                "X-PII-Replacements": str(
                    len(replacements)
                ),
            },
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Redaction failed: {exc}",
        )

    finally:
        # The response is streamed by FastAPI before cleanup
        # in normal operation. Temporary files are isolated
        # per request.
        pass


@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
):
    """
    Detect PII without creating a redacted document.

    Useful for testing and recruiter review.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided.",
        )

    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are supported.",
        )

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="pii_analysis_"
        )
    )

    input_path = temp_dir / "input.docx"

    try:
        with input_path.open("wb") as output_file:
            shutil.copyfileobj(
                file.file,
                output_file,
            )

        text = read_docx(input_path)

        detections = detect_all(text)

        return {
            "filename": file.filename,
            "characters": len(text),
            "total_detected": sum(
                len(values)
                for values in detections.values()
            ),
            "detections": detections,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {exc}",
        )