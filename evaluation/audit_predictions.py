import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


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
)


INPUT_FILE = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"


DETECTORS = {
    "PERSON": detect_person_names,
    "EMAIL": detect_emails,
    "PHONE": detect_phone_numbers,
    "COMPANY": detect_company_names,
    "SSN": detect_ssns,
    "CREDIT_CARD": detect_credit_cards,
    "DOB": detect_dates_of_birth,
    "IP_ADDRESS": detect_ip_addresses,
}


def main() -> None:
    print("Reading prospectus...")
    text = read_docx(INPUT_FILE)

    print(f"Characters loaded: {len(text)}")
    print()

    for pii_type, detector in DETECTORS.items():
        print("=" * 80)
        print(pii_type)
        print("=" * 80)

        # COMPANY uses the same filtering mode as evaluate.py.
        if pii_type == "COMPANY":
            predictions = detector(text, allowed_only=True)
        else:
            predictions = detector(text)

        print(f"Candidates detected: {len(predictions)}")
        print()

        if not predictions:
            print("No candidates detected.")
            print()
            continue

        for index, prediction in enumerate(predictions, start=1):
            print(f"{index:3}. {prediction}")

        print()


if __name__ == "__main__":
    main()