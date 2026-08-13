import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_ip_addresses


def test_detect_private_ipv4_address():
    text = "Client IP address: 192.168.1.10"

    result = detect_ip_addresses(text)

    assert result == ["192.168.1.10"]


def test_detect_multiple_ip_addresses():
    text = """
    Server: 10.0.0.25
    Gateway: 192.168.1.1
    """

    result = detect_ip_addresses(text)

    assert result == [
        "10.0.0.25",
        "192.168.1.1",
    ]


def test_detect_public_ipv4_address():
    text = "DNS server: 8.8.8.8"

    result = detect_ip_addresses(text)

    assert result == ["8.8.8.8"]


def test_invalid_ipv4_is_not_detected():
    text = "Invalid address: 256.300.999.1"

    result = detect_ip_addresses(text)

    assert result == []


def test_duplicate_ip_is_returned_once():
    text = """
    Client: 192.168.1.10
    Client again: 192.168.1.10
    """

    result = detect_ip_addresses(text)

    assert result == ["192.168.1.10"]


def test_normal_numbers_are_not_detected():
    text = """
    Date: 10.12.2025
    Amount: 4200.50
    Identifier: 123456789
    """

    result = detect_ip_addresses(text)

    assert result == []