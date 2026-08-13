from pathlib import Path

from src.document_reader import read_docx
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
from src.redactor import redact_docx


PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = (
    PROJECT_ROOT
    / "input"
    / "Red Herring Prospectus.docx"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "output"
    / "Redacted Red Herring Prospectus.docx"
)


def detect_all(text: str) -> dict[str, list[str]]:
    """
    Run every PII detector.
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


def main() -> None:
    print("=" * 70)
    print("PII REDACTION")
    print("=" * 70)

    print()
    print("Input:")
    print(INPUT_FILE)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input document not found: {INPUT_FILE}"
        )

    print()
    print("Reading document...")

    text = read_docx(INPUT_FILE)

    print(f"Characters loaded: {len(text):,}")

    print()
    print("Running detectors...")

    detections = detect_all(text)

    total = 0

    for pii_type, values in detections.items():
        count = len(values)
        total += count

        print(
            f"  {pii_type:15} {count:3} detected"
        )

    print()
    print(f"Total detected PII values: {total}")

    print()
    print("Generating fake replacements and redacting document...")

    replacements = redact_docx(
        input_file=INPUT_FILE,
        output_file=OUTPUT_FILE,
        detections=detections,
    )

    print()
    print("Redaction complete.")

    print()
    print("Replacement summary:")

    for original, replacement in replacements.items():
        print(
            f"  {original}  ->  {replacement}"
        )

    print()
    print("Output:")
    print(OUTPUT_FILE)

    print()
    print("=" * 70)
    print("SUCCESS")
    print("=" * 70)


if __name__ == "__main__":
    main()