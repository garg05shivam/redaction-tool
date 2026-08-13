import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_emails
def test_detect_single_email():
    text = "Contact us at hello@example.com"

    result = detect_emails(text)

    assert result == ["hello@example.com"]


def test_detect_multiple_emails():
    text = """
    Contact hello@example.com or support@example.org.
    """

    result = detect_emails(text)

    assert result == [
        "hello@example.com",
        "support@example.org",
    ]


def test_duplicate_email_is_returned_once():
    text = """
    Email: hello@example.com
    Please reply to hello@example.com
    """

    result = detect_emails(text)

    assert result == ["hello@example.com"]


def test_email_inside_normal_text():
    text = "The email address is user.name+test@example.co.in."

    result = detect_emails(text)

    assert result == ["user.name+test@example.co.in"]


def test_text_without_email():
    text = "There is no contact information here."

    result = detect_emails(text)

    assert result == []