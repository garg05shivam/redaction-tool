import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_credit_cards
from src.document_reader import read_docx


def main() -> None:
    input_file = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"

    document_text = read_docx(input_file)

    credit_cards = detect_credit_cards(document_text)

    print(f"Credit cards detected: {len(credit_cards)}")

    for card in credit_cards:
        print(card)


if __name__ == "__main__":
    main()