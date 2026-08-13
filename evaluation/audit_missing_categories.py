import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.document_reader import read_docx


INPUT_FILE = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"


PATTERNS = {
    "SSN": re.compile(
        r"\b\d{3}-\d{2}-\d{4}\b"
    ),

    "CREDIT_CARD": re.compile(
        r"\b(?:\d[ -]*?){13,19}\b"
    ),

    "DOB": re.compile(
        r"\b(?:"
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r"|"
        r"\d{1,2}\s+"
        r"(?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December)"
        r"\s+\d{4}"
        r")\b",
        re.IGNORECASE,
    ),

    "IP_ADDRESS": re.compile(
        r"\b"
        r"(?:25[0-5]|2[0-4]\d|1?\d?\d)"
        r"(?:\."
        r"(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}"
        r"\b"
    ),
}


def main() -> None:
    print("Reading prospectus...")
    text = read_docx(INPUT_FILE)

    print(f"Characters loaded: {len(text)}")
    print()

    for pii_type, pattern in PATTERNS.items():
        matches = pattern.findall(text)

        unique_matches = []
        seen = set()

        for match in matches:
            value = match.strip()

            if value.casefold() not in seen:
                seen.add(value.casefold())
                unique_matches.append(value)

        print("=" * 80)
        print(pii_type)
        print("=" * 80)
        print(f"Pattern candidates: {len(unique_matches)}")
        print()

        if not unique_matches:
            print("No pattern candidates found.")
        else:
            for index, value in enumerate(unique_matches, start=1):
                print(f"{index:3}. {value}")

        print()


if __name__ == "__main__":
    main()