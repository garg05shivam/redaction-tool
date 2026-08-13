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