import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_credit_cards, passes_luhn_checksum


def test_valid_luhn_number():
    assert passes_luhn_checksum("4111111111111111") is True


def test_invalid_luhn_number():
    assert passes_luhn_checksum("4111111111111112") is False


def test_detect_credit_card_with_spaces():
    text = "Card number: 4111 1111 1111 1111"

    result = detect_credit_cards(text)

    assert result == ["4111 1111 1111 1111"]


def test_detect_credit_card_with_hyphens():
    text = "Card: 4111-1111-1111-1111"

    result = detect_credit_cards(text)

    assert result == ["4111-1111-1111-1111"]


def test_invalid_card_is_not_detected():
    text = "Reference number: 4111 1111 1111 1112"

    result = detect_credit_cards(text)

    assert result == []


def test_duplicate_card_is_returned_once():
    text = """
    Card: 4111 1111 1111 1111
    Repeat: 4111 1111 1111 1111
    """

    result = detect_credit_cards(text)

    assert result == ["4111 1111 1111 1111"]