import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_ssns


def test_detect_standard_ssn():
    text = "SSN: 123-45-6789"

    result = detect_ssns(text)

    assert result == ["123-45-6789"]


def test_detect_multiple_ssns():
    text = """
    Person A: 123-45-6789
    Person B: 987-65-4321
    """

    result = detect_ssns(text)

    assert result == [
        "123-45-6789",
        "987-65-4321",
    ]


def test_duplicate_ssn_is_returned_once():
    text = """
    SSN: 123-45-6789
    Confirmed SSN: 123-45-6789
    """

    result = detect_ssns(text)

    assert result == ["123-45-6789"]


def test_plain_nine_digit_number_is_not_ssn():
    text = "Reference number: 123456789"

    result = detect_ssns(text)

    assert result == []


def test_wrong_ssn_format_is_not_detected():
    text = """
    1234-56-789
    12-345-6789
    123-456-789
    """

    result = detect_ssns(text)

    assert result == []