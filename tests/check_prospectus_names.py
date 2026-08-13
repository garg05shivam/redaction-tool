import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_person_names
from src.document_reader import read_docx


def main() -> None:
    input_file = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"

    print("Reading prospectus...")

    document_text = read_docx(input_file)

    print(f"Characters loaded: {len(document_text)}")
    print("Running person-name detection...")

    names = detect_person_names(document_text)

    print(f"Person names detected: {len(names)}")
    print()

    for index, name in enumerate(names, start=1):
        print(f"{index}. {name}")


if __name__ == "__main__":
    main()