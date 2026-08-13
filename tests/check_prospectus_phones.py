import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_phone_numbers
from src.document_reader import read_docx


def main() -> None:
    input_file = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"

    document_text = read_docx(input_file)

    phone_numbers = detect_phone_numbers(document_text)

    print(f"Phone numbers detected: {len(phone_numbers)}")

    for number in phone_numbers:
        print(number)


if __name__ == "__main__":
    main()