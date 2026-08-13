import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.document_reader import read_docx


INPUT_FILE = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"
GOLD_FILE = PROJECT_ROOT / "evaluation" / "gold_annotations.json"


def main() -> None:
    print("Reading prospectus...")
    text = read_docx(INPUT_FILE)

    print(f"Characters loaded: {len(text)}")
    print()

    with GOLD_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    annotations = data["annotations"]

    found = 0
    missing = 0

    print("Checking gold annotations...")
    print()

    for annotation in annotations:
        value = annotation["text"]
        pii_type = annotation["type"]

        if value in text:
            print(f"[FOUND]   {pii_type:12} | {value}")
            found += 1
        else:
            print(f"[MISSING] {pii_type:12} | {value}")
            missing += 1

    print()
    print("=" * 70)
    print(f"Total annotations : {len(annotations)}")
    print(f"Found             : {found}")
    print(f"Missing           : {missing}")

    if annotations:
        print(f"Coverage          : {found / len(annotations) * 100:.2f}%")

    print("=" * 70)


if __name__ == "__main__":
    main()