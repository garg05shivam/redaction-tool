import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Za-z0-9-]+"
    r"(?:\.[A-Za-z0-9-]+)+\b"
)


def detect_emails(text: str) -> list[str]:
    """mail retrun krega unique."""
    matches = EMAIL_PATTERN.findall(text)

    unique_emails = list(dict.fromkeys(matches))

    return unique_emails

PHONE_PATTERN = re.compile(
    r"""
    (?<!\d)
    (?:
        \+91[\s-]?[6-9]\d{9}

        |

        \+91[\s-]?\d{2,4}[\s-]?\d{6,8}

        |

     
        0\d{2,4}[\s-]\d{6,8}

        |

      
        [6-9]\d{9}
    )
    (?!\d)
    """,
    re.VERBOSE,
)
def detect_phone_numbers(text: str) -> list[str]:
    """Return unique phone-number candidates found in the text."""
    matches = PHONE_PATTERN.findall(text)

    unique_numbers = list(dict.fromkeys(matches))

    return unique_numbers

IP_PATTERN = re.compile(
    r"\b"
    r"(?:"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"\."
    r"){3}"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    r"\b"
)


def detect_ip_addresses(text: str) -> list[str]:
    """Return unique valid IPv4 addresses found in the text."""
    matches = IP_PATTERN.findall(text)

    unique_addresses = list(dict.fromkeys(matches))

    return unique_addresses

SSN_PATTERN = re.compile(
    r"(?<![\d-])"
    r"\d{3}-\d{2}-\d{4}"
    r"(?![\d-])"
)


def detect_ssns(text: str) -> list[str]:
    """Return unique SSN-format values found in the text."""
    matches = SSN_PATTERN.findall(text)

    unique_ssns = list(dict.fromkeys(matches))

    return unique_ssns


def passes_luhn_checksum(value: str) -> bool:
    """Return True when the numeric value passes the checksum."""
    digits = [int(character) for character in value if character.isdigit()]

    if not 13 <= len(digits) <= 19:
        return False

    checksum = 0
    double_digit = False

    for digit in reversed(digits):
        if double_digit:
            digit *= 2

            if digit > 9:
                digit -= 9

        checksum += digit
        double_digit = not double_digit

    return checksum % 10 == 0

CREDIT_CARD_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\d[ -]?){13,19}"
    r"(?!\d)"
)


def detect_credit_cards(text: str) -> list[str]:
    """Return unique credit-card candidates that pass Luhn validation."""
    candidates = CREDIT_CARD_PATTERN.findall(text)

    valid_cards = []

    for candidate in candidates:
        if passes_luhn_checksum(candidate):
            valid_cards.append(candidate)

    return list(dict.fromkeys(valid_cards))