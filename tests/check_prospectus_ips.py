import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_ip_addresses
from src.document_reader import read_docx


def main() -> None:
    input_file = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"

    document_text = read_docx(input_file)

    ip_addresses = detect_ip_addresses(document_text)

    print(f"IP addresses detected: {len(ip_addresses)}")

    for address in ip_addresses:
        print(address)


if __name__ == "__main__":
    main()