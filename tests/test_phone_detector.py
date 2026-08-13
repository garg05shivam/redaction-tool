import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_phone_numbers


def test_detect_indian_mobile_number():
    text = "Contact number: +91 9876543210"

    result = detect_phone_numbers(text)

    assert result == ["+91 9876543210"]


def test_detect_indian_mobile_without_country_code():
    text = "Phone: 9876543210"

    result = detect_phone_numbers(text)

    assert result == ["9876543210"]


def test_detect_indian_landline():
    text = "Telephone: +91 20 45053237"

    result = detect_phone_numbers(text)

    assert result == ["+91 20 45053237"]


def test_detect_hyphenated_number():
    text = "Call: 020-45053237"

    result = detect_phone_numbers(text)

    assert result == ["020-45053237"]


def test_duplicate_numbers_are_returned_once():
    text = """
    Phone: +91 9876543210
    Alternate phone: +91 9876543210
    """

    result = detect_phone_numbers(text)

    assert result == ["+91 9876543210"]

def test_numeric_identifier_is_not_phone_number():
    text = """
    Reference values: 000013004, 000011179, 000166136.
    """

    result = detect_phone_numbers(text)

    assert result == []