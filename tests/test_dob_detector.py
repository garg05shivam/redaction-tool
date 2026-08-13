import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_dates_of_birth


def test_detect_dob_with_slashes():
    text = "Date of Birth: 15/08/1998"

    result = detect_dates_of_birth(text)

    assert result == ["15/08/1998"]


def test_detect_dob_with_hyphens():
    text = "DOB: 15-08-1998"

    result = detect_dates_of_birth(text)

    assert result == ["15-08-1998"]


def test_detect_dob_with_month_name():
    text = "Birth Date: 15 August 1998"

    result = detect_dates_of_birth(text)

    assert result == ["15 August 1998"]


def test_detect_multiple_dobs():
    text = """
    DOB: 15/08/1998
    Date of Birth: 21 March 1995
    """

    result = detect_dates_of_birth(text)

    assert result == [
        "15/08/1998",
        "21 March 1995",
    ]


def test_duplicate_dob_is_returned_once():
    text = """
    DOB: 15/08/1998
    DOB again: 15/08/1998
    """

    result = detect_dates_of_birth(text)

    assert result == ["15/08/1998"]


def test_normal_date_is_not_dob():
    text = """
    Prospectus dated December 10, 2025.
    Incorporated on July 30, 1979.
    """

    result = detect_dates_of_birth(text)

    assert result == []