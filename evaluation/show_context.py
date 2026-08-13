import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.document_reader import read_docx


INPUT_FILE = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"


def show_context(text: str, value: str, window: int = 120) -> None:
    start = text.casefold().find(value.casefold())

    if start == -1:
        print(f"[NOT FOUND] {value}")
        return

    context_start = max(0, start - window)
    context_end = min(len(text), start + len(value) + window)

    context = text[context_start:context_end]

    print("-" * 80)
    print(f"Candidate: {value}")
    print("-" * 80)
    print(context)
    print()


def main() -> None:
    text = read_docx(INPUT_FILE)

    candidates = [
        "Electricals Private Limited",
        "Park IV Private Limited",
        "BSE Limited",
        "Federal Bank Limited",
        "KSH Infra Park VI Private Limited"
    ]

    for candidate in candidates:
        show_context(text, candidate)


if __name__ == "__main__":
    main()