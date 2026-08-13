from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from src.detectors import (
    detect_person_names,
    detect_emails,
    detect_phone_numbers,
    detect_company_names,
    detect_ssns,
    detect_credit_cards,
    detect_dates_of_birth,
    detect_ip_addresses,
    detect_addresses,
)

from src.document_reader import read_docx
from src.redactor import redact_docx


app = FastAPI(
    title="PII Detection and Redaction API",
    description=(
        "Detect personally identifiable information in DOCX "
        "documents and generate a redacted DOCX containing "
        "realistic fake replacements."
    ),
    version="1.0.0",
)


DOCX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument."
    "wordprocessingml.document"
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
    Run all supported PII detectors.

    Returns:
        Dictionary mapping PII type to detected values.
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

        "ADDRESS": detect_addresses(text),
    }


def validate_docx_upload(file: UploadFile) -> None:
    """
    Validate that an uploaded file is a DOCX document.
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


def cleanup_directory(directory: Path) -> None:
    """
    Remove a temporary directory after the response has
    finished sending.
    """

    try:
        shutil.rmtree(
            directory,
            ignore_errors=True,
        )
    except Exception:
        pass



@app.post("/detect")
async def detect_and_redact(
    file: UploadFile = File(...),
):
    """
    Upload a DOCX document.

    Processing steps:

    1. Save the uploaded DOCX.
    2. Read its text.
    3. Detect supported PII.
    4. Generate fake replacements.
    5. Create a redacted DOCX.
    6. Return the redacted DOCX.

    Supported PII types:

    - PERSON
    - EMAIL
    - PHONE
    - COMPANY
    - SSN
    - CREDIT_CARD
    - DOB
    - IP_ADDRESS
    - ADDRESS
    """

    validate_docx_upload(file)

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="pii_redaction_"
        )
    )

    input_path = temp_dir / "input.docx"
    output_path = temp_dir / "redacted.docx"

    try:

        with input_path.open("wb") as output_file:
            shutil.copyfileobj(
                file.file,
                output_file,
            )

        text = read_docx(input_path)

        detections = detect_all(text)

        total_detected = sum(
            len(values)
            for values in detections.values()
        )

        replacements = redact_docx(
            input_file=input_path,
            output_file=output_path,
            detections=detections,
        )

        if not output_path.exists():
            raise HTTPException(
                status_code=500,
                detail=(
                    "Redaction completed but the "
                    "redacted document was not generated."
                ),
            )


        cleanup_task = BackgroundTask(
            cleanup_directory,
            temp_dir,
        )

        output_filename = (
            "Redacted_" + file.filename
        )

        return FileResponse(
            path=output_path,
            media_type=DOCX_MEDIA_TYPE,
            filename=output_filename,
            headers={
                "X-PII-Total-Detected": str(
                    total_detected
                ),
                "X-PII-Replacements": str(
                    len(replacements)
                ),
            },
            background=cleanup_task,
        )

    except HTTPException:
        cleanup_directory(temp_dir)
        raise

    except Exception as exc:
        cleanup_directory(temp_dir)

        raise HTTPException(
            status_code=500,
            detail=f"Redaction failed: {exc}",
        )

    finally:
        await file.close()


@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
):
    """
    Upload a DOCX and return detected PII without creating
    a redacted document.

    Useful for testing and demonstration.
    """

    validate_docx_upload(file)

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

        total_detected = sum(
            len(values)
            for values in detections.values()
        )


        return {
            "filename": file.filename,
            "characters": len(text),
            "total_detected": total_detected,
            "detections": detections,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {exc}",
        )

    finally:
        await file.close()
        cleanup_directory(temp_dir)