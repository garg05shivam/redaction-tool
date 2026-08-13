import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_company_names


def test_detect_company_name():
    text = "KSH International Limited was incorporated in Maharashtra."

    result = detect_company_names(text)

    assert "KSH International Limited" in result


def test_detect_bank_company():
    text = "HDFC Bank Limited provides banking services."

    result = detect_company_names(text)

    assert "HDFC Bank Limited" in result


def test_detect_private_company():
    text = "Bhandary Metal Extrusion Private Limited was incorporated."

    result = detect_company_names(text)

    assert "Bhandary Metal Extrusion Private Limited" in result


def test_person_name_is_not_company():
    text = "Kushal Subbayya Hegde is a director."

    result = detect_company_names(text)

    assert "Kushal Subbayya Hegde" not in result


def test_document_title_is_not_company():
    text = "RED HERRING PROSPECTUS"

    result = detect_company_names(text)

    assert "RED HERRING PROSPECTUS" not in result


def test_generic_financial_term_is_not_company():
    text = "Mutual Funds and Equity Shares"

    result = detect_company_names(text)

    assert "Mutual Funds" not in result
    assert "Equity Shares" not in result


def test_duplicate_company_is_returned_once():
    text = """
    KSH International Limited was incorporated in 1979.
    KSH International Limited operates manufacturing facilities.
    """

    result = detect_company_names(text)

    matching = [
        company
        for company in result
        if company.casefold() == "ksh international limited"
    ]

    assert len(matching) == 1

def test_generic_financial_terms_are_not_companies():
    text = """
    Capital Employed
    Working Capital Days
    Financial Information
    State Insurance
    """

    result = detect_company_names(text)

    assert "Capital Employed" not in result
    assert "Working Capital Days" not in result
    assert "Financial Information" not in result
    assert "State Insurance" not in result


def test_company_with_strong_legal_suffix_is_detected():
    text = """
    Emirates Transformer & Switchgear Limited
    HDFC Bank Limited
    """

    result = detect_company_names(text)

    assert "Emirates Transformer & Switchgear Limited" in result
    assert "HDFC Bank Limited" in result

def test_bank_phrase_is_not_company():
    text = "Bank Balances and Advances"

    result = detect_company_names(text)

    assert "Bank Balances and Advances" not in result


def test_refund_bank_is_not_company():
    text = "the Refund Bank"

    result = detect_company_names(text)

    assert "the Refund Bank" not in result


def test_bank_facility_is_not_company():
    text = "Long Term Bank Facilities"

    result = detect_company_names(text)

    assert "Long Term Bank Facilities" not in result


def test_regulator_is_not_company():
    text = "Securities and Exchange Board of India"

    result = detect_company_names(text)

    assert "Securities and Exchange Board of India" not in result


def test_law_is_not_company():
    text = "Securities and Exchange Board of India Act"

    result = detect_company_names(text)

    assert "Securities and Exchange Board of India Act" not in result


def test_real_bank_is_company():
    text = "HDFC Bank Limited"

    result = detect_company_names(text)

    assert "HDFC Bank Limited" in result

def test_duplicate_company_span_is_cleaned():
    text = "HDFC Bank Limited HDFC Bank Limited"

    result = detect_company_names(text)

    assert "HDFC Bank Limited" in result
    assert "HDFC Bank Limited HDFC Bank Limited" not in result


def test_leading_article_is_removed():
    text = "the HDFC Bank Limited"

    result = detect_company_names(text)

    assert "HDFC Bank Limited" in result
    assert "the HDFC Bank Limited" not in result


def test_trailing_context_is_removed():
    text = "HDFC Bank Limited Registered Brokers"

    result = detect_company_names(text)

    assert "HDFC Bank Limited" in result
    assert "HDFC Bank Limited Registered Brokers" not in result


def test_regulator_with_leading_article_is_rejected():
    text = "the Securities and Exchange Board of India"

    result = detect_company_names(text)

    assert "Securities and Exchange Board of India" not in result

def test_legal_pattern_detects_full_private_company_name():
    text = """
    Kushal Electricals Private Limited operates in Maharashtra.
    """

    result = detect_company_names(text)

    assert "Kushal Electricals Private Limited" in result


def test_legal_pattern_detects_full_limited_company_name():
    text = """
    Emirates Transformer & Switchgear Limited is a company.
    """

    result = detect_company_names(text)

    assert "Emirates Transformer & Switchgear Limited" in result


def test_legal_pattern_detects_llp():
    text = """
    Kirtane & Pandit LLP is mentioned in the prospectus.
    """

    result = detect_company_names(text)

    assert "Kirtane & Pandit LLP" in result

def test_context_prefix_is_removed():
    text = """
    Offer MUFG Intime India Private Limited
    Formerly Link Intime India Private Limited
    """

    result = detect_company_names(text)

    assert "MUFG Intime India Private Limited" in result
    assert "Link Intime India Private Limited" in result

    assert "Offer MUFG Intime India Private Limited" not in result
    assert "Formerly Link Intime India Private Limited" not in result


def test_duplicate_context_does_not_become_company():
    text = """
    HDFC Bank Limited HDFC Bank Limited
    """

    result = detect_company_names(text)

    assert "HDFC Bank Limited" in result
    assert "HDFC Bank Limited HDFC Bank Limited" not in result


def test_incomplete_company_names_are_rejected():
    text = """
    Private Limited
    India Limited
    Investment Private Limited
    """

    result = detect_company_names(text)

    assert "Private Limited" not in result
    assert "India Limited" not in result
    assert "Investment Private Limited" not in result

def test_detect_company_name():
    text = "KSH International Limited was incorporated."

    result = detect_company_names(text)

    assert "KSH International Limited" in result


def test_detect_bank_company():
    text = "HDFC Bank Limited provides banking services."

    result = detect_company_names(text)

    assert "HDFC Bank Limited" in result


def test_detect_private_company():
    text = "Bhandary Metal Extrusion Private Limited was incorporated."

    result = detect_company_names(text)

    assert "Bhandary Metal Extrusion Private Limited" in result


def test_person_name_is_not_company():
    text = "Kushal Subbayya Hegde is a director."

    result = detect_company_names(text)

    assert "Kushal Subbayya Hegde" not in result


def test_document_context_is_not_company():
    text = "Offer Escrow Collection Bank"

    result = detect_company_names(text)

    assert "Offer Escrow Collection Bank" not in result


def test_regulator_is_not_company():
    text = "Securities and Exchange Board of India"

    result = detect_company_names(text)

    assert "Securities and Exchange Board of India" not in result


def test_duplicate_company_is_returned_once():
    text = """
    KSH International Limited was incorporated.
    KSH International Limited operates manufacturing facilities.
    """

    result = detect_company_names(text)

    matching = [
        company
        for company in result
        if company.casefold() == "ksh international limited"
    ]

    assert len(matching) == 1

def test_generic_company_fragment_is_rejected():
    text = """
    Securities Limited
    Advisory Private Limited
    """

    result = detect_company_names(text)

    assert "Securities Limited" not in result
    assert "Advisory Private Limited" not in result