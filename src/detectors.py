import re
import spacy
NER_MODEL_NAME = "en_core_web_sm"
PERSON_REJECTION_TERMS = {
    "limited",
    "private",
    "company",
    "corporation",
    "trust",
    "bank",
    "hospital",
    "facility",
    "electricals",
    "huf",

    "shareholder",
    "shareholders",
    "promoter",
    "promoters",
    "director",
    "directors",
    "personnel",
    "managerial",
    "transfer",
    "secondary",
    "selling",
    "reference",
    "rate",
    "amount",
    "price",
    "offer",
    "bidders",
    "bidder",
    "bid",
    "listing",
    "registrar",
    "website",
    "account",
    "particulars",
    "description",
    "schedule",
    "acknowledgement",
    "circulars",
    "defaulter",
    "dues",
    "branch",
    "broker",
    "brokerage",
    "escrow",
    "collection",
    "agent",
    "agents",
    "registered",

    "mutual",
    "funds",
    "financial",
    "operational",
    "measures",
    "ebitda",
    "gigawatt",
    "gigawatt-hour",
    "megawatt",
    "kilometers",
    "air",
    "conditioning",
    "mega",
    "volt-amperes",
    "photovoltaic",
    "photo",
    "voltaic",
    "energy",
    "power",
    "dfi",

    "taluka",
    "village",
    "marg",
    "hospital",
    "shivajinagar",
    "reclamation",
    "churchgate",
    "khalumbre",
    "industrial",
    "park",

    "acknowledgement",
    "slip",
    "schedule",
    "description",
    "red",

    "gigawatt",
    "gwh",
    "hvdc",
    "megavolt-amperes",
    "megawatt",
    "mww",

    "s",
    "no",

    "offer-related",
    "related",
    "widely",
    "circulated",
    "marathi",
    "daily",
    "newspaper",
    "kisan",
    "urja",
    "suraksha",
    "dp",
    "id",

    "taluka",
    "pune",
    "mumbai",
    "marg",
    "road",
    "lane",
    "nagar",
    "village",
    "park",
    "industrial",
    "house",
    "apartment",
    "flat",
    "showroom",
    "chambers",
    "bhavan",
    "complex",
    "east",
    "west",
    "north",
    "south",
    "gymkhana",
    "colony",
    "monte",

    "corrigenda",
    "thereto",
    "circuit",
    "kilometers",
    "branch",
    "particulars",
    "description",
    "nuvama",
    "s.",
    "no.",
    "bo",
}
COMPANY_STRONG_SUFFIXES = {
    "limited",
    "ltd",
    "llp",
    "inc",
    "incorporated",
    "corporation",
    "corp",
}

COMPANY_LEGAL_PHRASES = {
    "private limited",
    "pvt ltd",
}

COMPANY_BUSINESS_INDICATORS = {
    "bank",
    "securities",
    "leasing",
    "investments",
}
def load_ner_model():
    """Load the spaCy English model used for person/entity detection."""
    return spacy.load(NER_MODEL_NAME)

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

DOB_PATTERN = re.compile(
    r"""
    \b
    (?:
        date\s+of\s+birth
        |
        dob
        |
        birth\s+date
    )
    \s*
    (?:
        :
        |
        -
        |
        \s
    )
    \s*
    (
        \d{1,2}[/-]\d{1,2}[/-]\d{4}
        |
        \d{1,2}\s+
        (?:January|February|March|April|May|June|July|August|September|October|November|December)
        \s+
        \d{4}
    )
    \b
    """,
    re.IGNORECASE | re.VERBOSE,
)


def detect_dates_of_birth(text: str) -> list[str]:
    """Return dates explicitly associated with birth-date terminology."""
    matches = DOB_PATTERN.findall(text)

    return list(dict.fromkeys(matches))

def _looks_like_person_name(name: str) -> bool:
    """Apply conservative rules to a spaCy PERSON candidate."""
    cleaned = " ".join(name.split())

    if not cleaned:
        return False

    words = cleaned.split()

    # A full name normally contains at least two words.
    if len(words) < 2:
        return False

    # Avoid unusually long NER spans.
    if len(words) > 6:
        return False

    # Names should not contain digits.
    if any(character.isdigit() for character in cleaned):
        return False

    # Reject email, URL, and table-like fragments.
    if any(symbol in cleaned for symbol in "@:/|"):
        return False

    normalized_words = set()

    for word in words:
        cleaned_word = word.strip(".,()[]{}'\"")

        for part in cleaned_word.split("-"):
            if part:
                normalized_words.add(part.lower())

    # Reject known non-person terminology.
    if normalized_words & PERSON_REJECTION_TERMS:
        return False

    # Reject candidates beginning with common document/address words.
    first_word = words[0].strip(".,()[]{}'\"").lower()

    if first_word in {
        "a",
        "an",
        "the",
        "of",
        "and",
        "or",
        "to",
        "in",
    }:
        return False

    # Reject location/address phrases.
    address_indicators = {
        "taluka",
        "village",
        "marg",
        "road",
        "lane",
        "nagar",
        "park",
        "industrial",
        "complex",
        "colony",
        "hospital",
        "reclamation",
    }

    if normalized_words & address_indicators:
        return False

    # Reject technical/document phrases.
    technical_indicators = {
        "schedule",
        "mega",
        "volt",
        "amperes",
        "megawatt",
        "gigawatt",
        "gwh",
        "hvdc",
        "mww",
    }

    if normalized_words & technical_indicators:
        return False

    # Every word must contain alphabetic characters.
    if not all(
        any(character.isalpha() for character in word)
        for word in words
    ):
        return False

    return True

def detect_person_names(text: str) -> list[str]:
    """Return filtered unique PERSON names detected by spaCy."""
    nlp = load_ner_model()

    chunk_size = 50000
    names = []

    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]

        document = nlp(chunk)

        for entity in document.ents:
            if entity.label_ != "PERSON":
                continue

            name = " ".join(entity.text.split())

            if _looks_like_person_name(name):
                names.append(name)

    unique_names = []
    seen = set()

    for name in names:
        key = name.casefold()

        if key not in seen:
            seen.add(key)
            unique_names.append(name)

    return unique_names


def _looks_like_company_name(name: str) -> bool:
    """Return True for conservative company/organization candidates."""
    cleaned = " ".join(name.split()).strip()

    if not cleaned:
        return False

    normalized = cleaned.casefold()
    words = normalized.split()
    generic_company_fragments = {
        "securities limited",
        "advisory private limited",
    }

    if normalized in generic_company_fragments:
        return False

    if len(words) < 2:
        return False

    if len(words) > 12:
        return False

    # Reject obvious document/table fragments.
    if any(symbol in cleaned for symbol in ["@", "|", "/"]):
        return False

    # Reject common prospectus context words.
    rejection_terms = {
        "offer",
        "escrow",
        "collection",
        "account",
        "public",
        "refund",
        "registered",
        "brokers",
        "sponsor",
        "banks",
        "syndicate",
        "members",
        "shareholders",
        "lead",
        "managers",
        "registrar",
        "telephone",
        "email",
        "collectively",
        "ground",
        "floor",
        "independent",
        "director",
        "directors",
    }

    normalized_words = set(words)

    if normalized_words & rejection_terms:
        return False

    # Reject regulatory/legal bodies that aren't company PII.
    regulator_prefixes = (
        "securities and exchange board",
        "reserve bank of india",
        "insurance regulatory and development authority",
        "national payments corporation",
        "national securities depository",
        "government of india",
        "ministry of",
    )

    if normalized.startswith(regulator_prefixes):
        return False

    # Strong legal entity indicators.
    strong_suffixes = {
        "limited",
        "ltd",
        "llp",
        "corporation",
        "corp",
    }

    if any(
        normalized.endswith(f" {suffix}")
        for suffix in strong_suffixes
    ):
        return True

    if normalized.endswith(" private limited"):
        return True

    if normalized.endswith(" pvt ltd"):
        return True

    return False

def _clean_company_candidate(name: str) -> str:
    cleaned = " ".join(name.split()).strip()

    for prefix in ("the ", "a ", "an "):
        if cleaned.casefold().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()

    trailing_phrases = (
        " independent director(s)",
        " registered brokers",
        " ground floor",
        " public offer account",
        " stock",
    )

    lowered = cleaned.casefold()

    for phrase in trailing_phrases:
        if lowered.endswith(phrase):
            cleaned = cleaned[:-len(phrase)].strip()
            lowered = cleaned.casefold()

    words = cleaned.split()

    if len(words) % 2 == 0:
        midpoint = len(words) // 2

        first_half = " ".join(words[:midpoint])
        second_half = " ".join(words[midpoint:])

        if first_half.casefold() == second_half.casefold():
            cleaned = first_half

    return cleaned
def _deduplicate_company_names(companies: list[str]) -> list[str]:
    cleaned = []

    for company in companies:
        company = " ".join(company.split()).strip()

        if company:
            cleaned.append(company)

    unique = {}
    
    for company in cleaned:
        key = company.casefold()

        if key not in unique:
            unique[key] = company

    candidates = list(unique.values())

    result = []

    for candidate in candidates:
        candidate_key = candidate.casefold()

        contained_in_longer = False

        for other in candidates:
            other_key = other.casefold()

            if (
                candidate_key != other_key
                and candidate_key in other_key
                and len(other_key) > len(candidate_key)
            ):
                contained_in_longer = True
                break

        if not contained_in_longer:
            result.append(candidate)

    return result

def detect_company_names(text: str) -> list[str]:
    """Return unique company names ."""
    nlp = load_ner_model()

    companies = []
    chunk_size = 50000

    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]

        document = nlp(chunk)

        for entity in document.ents:
            if entity.label_ != "ORG":
                continue

            company = _clean_company_candidate(entity.text)

            if _looks_like_company_name(company):
                companies.append(company)

    return _deduplicate_company_names(companies)

def _clean_legal_company_candidate(name: str) -> str:
    """Remove common document/context prefixes from a company candidate."""
    cleaned = " ".join(name.split()).strip()

    prefixes = (
        "Offer ",
        "Formerly ",
        "Company ",
        "Collectively, ",
        "Shareholders ",
        "Anchor Investor. ",
        "Sponsor Banks ",
        "Syndicate Members ",
        "Public Offer Account Bank ",
        "REGISTRAR TO THE OFFER ",
        "EMAIL AND TELEPHONE ",
        "TELEPHONE AND EMAIL ",
    )

    changed = True

    while changed:
        changed = False

        for prefix in prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                changed = True

    return cleaned

def detect_legal_company_names(text: str) -> list[str]:
    """Detect company names using common legal entity suffixes."""
    patterns = [
        r"\b(?:[A-Z][A-Za-z&.,'()-]*\s+){1,7}Private Limited\b",
        r"\b(?:[A-Z][A-Za-z&.,'()-]*\s+){1,7}Limited\b",
        r"\b(?:[A-Z][A-Za-z&.,'()-]*\s+){1,7}Corporation\b",
        r"\b(?:[A-Z][A-Za-z&.,'()-]*\s+){1,7}LLP\b",
        r"\b(?:[A-Z][A-Za-z&.,'()-]*\s+){1,7}Ltd\.?\b",
    ]

    companies = []

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            company = " ".join(match.group(0).split()).strip()

            if _looks_like_company_name(company):
                companies.append(company)

    return companies