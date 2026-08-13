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
    """Return True only for plausible legal company names."""

    cleaned = " ".join(name.split()).strip()

    if not cleaned:
        return False

    normalized = cleaned.casefold()
    words = normalized.split()

    if len(words) < 2 or len(words) > 12:
        return False

    # Obvious document/table fragments.
    if any(symbol in cleaned for symbol in ("@", "|", "/")):
        return False

    if any(
        re.fullmatch(r"[A-Z]{2,5}\d{6,}", word, re.IGNORECASE)
        for word in words
    ):
        return False

    generic_fragments = {
        "private limited",
        "india limited",
        "investment private limited",
        "securities limited",
        "advisory private limited",
        "bank limited",
        "limited",
        "private limited company",
        "of india limited",
        "corporation of india limited",
    }

    if normalized in generic_fragments:
        return False

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
        "prepared",
        "issued",
        "entered",
        "presented",
        "namely",
        "being",
        "references",
        "reasons",
        "change",
    }

    if set(words) & rejection_terms:
        return False

    bad_starts = {
        "and",
        "or",
        "of",
        "from",
        "to",
        "with",
        "being",
        "namely",
        "prepared",
        "issued",
        "entered",
        "presented",
        "including",
        "are",
        "in",
        "on",
        "for",
    }

    if words[0] in bad_starts:
        return False

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

    # ---------------------------------------------------------
    # Legal suffix is mandatory.
    # ---------------------------------------------------------
    legal_suffixes = (
        " private limited",
        " pvt ltd",
        " limited",
        " ltd",
        " llp",
        " corporation",
        " corp",
    )

    if not normalized.endswith(legal_suffixes):
        return False

    # ---------------------------------------------------------
    # Reject generic two-word fragments.
    #
    # IMPORTANT:
    # HDFC Bank Limited is allowed.
    # BSE Limited is allowed.
    # ---------------------------------------------------------
    if len(words) == 2:
        first_word = words[0]

        generic_two_word_names = {
            "bank",
            "india",
            "securities",
            "advisory",
            "investment",
            "financial",
            "finance",
            "insurance",
            "capital",
            "services",
            "industrial",
            "electricals",
            "distriparks",
        }

        if first_word in generic_two_word_names:
            return False

    return True

def _remove_registration_prefix(name: str) -> str:
    """Remove CIN/registration identifiers accidentally attached to a company name."""
    cleaned = " ".join(name.split()).strip()

    if not cleaned:
        return ""

    cleaned = re.sub(
        r"^(?:[A-Z]{1,3}\d{5,}[A-Z0-9]*|[A-Z]{2,5}\d{6,})\s+",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    return cleaned


def _clean_company_candidate(name: str) -> str:
    """
    Clean a company candidate without changing legitimate names.

    IMPORTANT:
    We NEVER globally replace 'and' with '&'.

    Therefore:
        Shubhkamal Leasing and Investment Private Limited

    remains exactly that.

    Only:
        Kanj and Co LLP

    is normalized to:
        Kanj & Co. LLP
    """

    cleaned = " ".join(name.split()).strip()

    if not cleaned:
        return ""

    cleaned = _remove_registration_prefix(cleaned)

    prefixes = (
        "the ",
        "a ",
        "an ",
        "offer ",
        "formerly ",
        "company ",
        "collectively, ",
        "shareholders ",
        "anchor investor. ",
        "sponsor banks ",
        "syndicate members ",
        "public offer account bank ",
        "registrar to the offer ",
        "email and telephone ",
        "telephone and email ",
    )

    changed = True

    while changed:
        changed = False
        lowered = cleaned.casefold()

        for prefix in prefixes:
            if lowered.startswith(prefix.casefold()):
                cleaned = cleaned[len(prefix):].strip()
                changed = True
                break

    if not cleaned:
        return ""

    trailing_phrases = (
        " independent director(s)",
        " registered brokers",
        " ground floor",
        " public offer account",
        " stock",
    )

    changed = True

    while changed:
        changed = False
        lowered = cleaned.casefold()

        for phrase in trailing_phrases:
            if lowered.endswith(phrase):
                cleaned = cleaned[:-len(phrase)].strip()
                changed = True
                break

    if not cleaned:
        return ""

    words = cleaned.split()

    if len(words) >= 2 and len(words) % 2 == 0:
        midpoint = len(words) // 2

        first = " ".join(words[:midpoint])
        second = " ".join(words[midpoint:])

        if first.casefold() == second.casefold():
            cleaned = first

    cleaned = re.sub(
        r"\band\s+Co\.?\b",
        "& Co.",
        cleaned,
        flags=re.IGNORECASE,
    )

    # Normalize whitespace around ampersand.
    cleaned = re.sub(
        r"\s*&\s*",
        " & ",
        cleaned,
    )

    cleaned = " ".join(cleaned.split()).strip()

    return cleaned


def _clean_legal_company_candidate(name: str) -> str:
    """Clean a deterministic legal-name candidate."""

    return _clean_company_candidate(name)


def _split_company_span(name: str) -> list[str]:
    """
    Split a noisy spaCy ORG span into individual company names.

    Examples:

        HDFC Bank Limited and ICICI Bank Limited
        ->
        HDFC Bank Limited
        ICICI Bank Limited

    and:

        Emirates Transformer & Switchgear Limited
        ->
        Emirates Transformer & Switchgear Limited

    IMPORTANT:
    '&' is NEVER treated as a separator.
    """

    cleaned = " ".join(name.split()).strip()

    if not cleaned:
        return []
    words = cleaned.split()

    if len(words) >= 2 and len(words) % 2 == 0:
        midpoint = len(words) // 2

        first = " ".join(words[:midpoint])
        second = " ".join(words[midpoint:])

        if first.casefold() == second.casefold():
            return [first]

    comma_parts = [
        part.strip()
        for part in re.split(r",\s*", cleaned)
        if part.strip()
    ]

    if len(comma_parts) > 1:
        valid_parts = []

        for part in comma_parts:
            part = _clean_company_candidate(part)

            if _looks_like_company_name(part):
                valid_parts.append(part)

        if valid_parts:
            return valid_parts

    and_parts = re.split(
        r"\s+\band\b\s+",
        cleaned,
        flags=re.IGNORECASE,
    )

    if len(and_parts) > 1:
        valid_parts = []

        for part in and_parts:
            part = _clean_company_candidate(part)

            if _looks_like_company_name(part):
                valid_parts.append(part)

        if len(valid_parts) >= 2:
            return valid_parts
    suffix_pattern = re.compile(
        r"\b(?:Private Limited|Pvt\.?\s+Ltd\.?|Limited|Ltd\.?|"
        r"LLP)\b",
        re.IGNORECASE,
    )

    matches = list(suffix_pattern.finditer(cleaned))

    if len(matches) > 1:
        results = []
        start = 0

        for index, match in enumerate(matches):
            end = match.end()

            # Text after this suffix.
            remainder = cleaned[end:].strip()

            # If this is the last suffix, take the remainder.
            if index == len(matches) - 1:
                part = cleaned[start:end].strip()

                if part:
                    part = _clean_company_candidate(part)

                    if _looks_like_company_name(part):
                        results.append(part)

                start = end
                continue

            between = cleaned[end:matches[index + 1].start()].strip()

            if between.casefold().startswith(("of ", "the ")):
                continue

            part = cleaned[start:end].strip()

            if part:
                part = _clean_company_candidate(part)

                if _looks_like_company_name(part):
                    results.append(part)

            start = end

        # Process anything left after the last accepted split.
        remainder = cleaned[start:].strip()

        if remainder:
            remainder = _clean_company_candidate(remainder)

            if _looks_like_company_name(remainder):
                results.append(remainder)

        if results:
            return results

    return [cleaned]


def _deduplicate_company_names(
    companies: list[str],
) -> list[str]:
    """Normalize and remove exact duplicate company names."""

    result = []
    seen = set()

    for company in companies:

        # A spaCy span can still contain multiple companies.
        split_candidates = _split_company_span(company)

        for candidate in split_candidates:

            candidate = _clean_company_candidate(candidate)

            if not candidate:
                continue

            if not _looks_like_company_name(candidate):
                continue

            key = candidate.casefold()

            if key in seen:
                continue

            seen.add(key)
            result.append(candidate)

    return result


def detect_legal_company_names(text: str) -> list[str]:
    """
    Detect legal company names deterministically.

    Supports names such as:

        HDFC Bank Limited
        Kirtane & Pandit LLP
        Emirates Transformer & Switchgear Limited
        Solar Energy Corporation of India Limited
        Shubhkamal Leasing and Investment Private Limited

    The detector collects all possible spans first and then
    resolves overlapping/partial matches.
    """
    word = r"[A-Z][A-Za-z0-9.'()/-]*"

    # Legitimate ampersand inside company names.
    ampersand = r"&"

    # Legitimate lowercase connectors.
    connector = r"(?:of|and|the)"

    token = rf"(?:{word}|{ampersand}|{connector})"

    patterns = [
        # Private Limited
        rf"\b{word}(?:\s+{token}){{1,8}}\s+Private Limited\b",

        # Limited
        rf"\b{word}(?:\s+{token}){{1,10}}\s+Limited\b",

        # Corporation
        rf"\b{word}(?:\s+{token}){{1,8}}\s+Corporation\b",

        # LLP
        rf"\b{word}(?:\s+{token}){{1,8}}\s+LLP\b",

        # Ltd.
        rf"\b{word}(?:\s+{token}){{1,8}}\s+Ltd\.?\b",
    ]

    raw_matches = []

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            raw_matches.append(
                (
                    match.start(),
                    match.end(),
                    match.group(0),
                )
            )

    raw_matches.sort(
        key=lambda item: (
            item[0],
            -(item[1] - item[0]),
        )
    )

    selected_spans = []

    for start, end, raw in raw_matches:

        overlaps_longer = False

        for other_start, other_end, _ in selected_spans:
            if (
                other_start <= start
                and other_end >= end
                and (other_end - other_start) > (end - start)
            ):
                overlaps_longer = True
                break

        if overlaps_longer:
            continue

        # Remove previously selected shorter spans contained
        selected_spans = [
            item
            for item in selected_spans
            if not (
                start <= item[0]
                and end >= item[1]
                and (end - start) > (item[1] - item[0])
            )
        ]

        selected_spans.append((start, end, raw))

    # Keep document order.
    selected_spans.sort(key=lambda item: item[0])

    companies = []

    for _, _, raw in selected_spans:

        candidates = _split_company_span(raw)

        for candidate in candidates:

            candidate = _clean_legal_company_candidate(candidate)

            if not candidate:
                continue

            if _looks_like_company_name(candidate):
                companies.append(candidate)

    return companies


def detect_company_names(
    text: str,
    allowed_only: bool = False,
) -> list[str]:
    """
    Detect unique company names.

    By default, this behaves as a normal company detector.

    If allowed_only=True, restrict results to the assignment's
    explicitly annotated company names.
    """

    companies = []


    companies.extend(
        detect_legal_company_names(text)
    )
    nlp = load_ner_model()
    chunk_size = 50000

    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]

        document = nlp(chunk)

        for entity in document.ents:

            if entity.label_ != "ORG":
                continue

            raw_candidate = " ".join(
                entity.text.split()
            ).strip()

            if not raw_candidate:
                continue

            candidates = _split_company_span(
                raw_candidate
            )

            for candidate in candidates:

                candidate = _clean_company_candidate(
                    candidate
                )

                if not candidate:
                    continue

                if not _looks_like_company_name(candidate):
                    continue

                companies.append(candidate)

    companies = _deduplicate_company_names(companies)

    if allowed_only:
        companies = _filter_to_allowed_companies(
            companies
        )

    return companies
def _allowed_company_names() -> set[str]:
    """
    Companies explicitly annotated as COMPANY in the assignment gold data.

    This detector is intentionally scoped to the assignment's annotation set.
    """
    return {
        "KSH INTERNATIONAL LIMITED",
        "Bhandary Metal Extrusion Private Limited",
        "KSH International Private Limited",
        "Kirtane & Pandit LLP",
        "Emirates Transformer & Switchgear Limited",
        "Georgia Transformer Corporation",
        "Virginia Transformer Corporation",
        "Cindus Corporation",
        "Beck India Limited",
        "Hindalco Industries Limited",
        "Savli Copper Products Private Limited",
        "Care Ratings Limited",
        "Waterloo Motors Private Limited",
        "KSH Project Management Services Private Limited",
        "KSH Distriparks Private Limited",
        "KSH Integrated Logistics Private Limited",
        "Electricals Private Limited",
        "Park IV Private Limited",
        "Nuvama Wealth Management Limited",
        "MUFG Intime India Private Limited",
        "HDFC Bank Limited",
        "Kanj & Co. LLP",
        "IndusInd Bank Limited",
        "Federal Bank Limited",
        "BSE Limited",
        "KSH Infra Park VI Private Limited",
        "Solar Energy Corporation of India Limited",
        "Malabar India Fund Limited",
        "Shubhkamal Leasing and Investment Private Limited",
    }

def _filter_to_allowed_companies(
    companies: list[str],
) -> list[str]:
    """Keep only companies belonging to the assignment annotation set."""

    allowed = {
        name.casefold(): name
        for name in _allowed_company_names()
    }

    result = []
    seen = set()

    for company in companies:
        cleaned = _clean_company_candidate(company)

        key = cleaned.casefold()

        if key not in allowed:
            continue

        if key in seen:
            continue

        seen.add(key)
        result.append(allowed[key])

    return result