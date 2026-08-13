import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.detectors import detect_person_names


def test_detect_person_name():
    text = "Kushal Subbayya Hegde is a director."

    result = detect_person_names(text)

    assert "Kushal Subbayya Hegde" in result


def test_detect_multiple_people():
    text = """
    Kushal Subbayya Hegde met Rajesh Kushal Hegde.
    """

    result = detect_person_names(text)

    assert "Kushal Subbayya Hegde" in result
    assert "Rajesh Kushal Hegde" in result


def test_company_is_not_expected_as_person():
    text = "KSH International Limited is the company."

    result = detect_person_names(text)

    assert "KSH International Limited" not in result


def test_duplicate_person_is_returned_once():
    text = """
    Kushal Subbayya Hegde is a director.
    Later, Kushal Subbayya Hegde is mentioned again.
    """

    result = detect_person_names(text)

    assert result.count("Kushal Subbayya Hegde") == 1


def test_single_word_entity_is_not_automatically_accepted():
    text = "Offer Directors Promoters Fraud"

    result = detect_person_names(text)

    assert "Offer" not in result
    assert "Directors" not in result
    assert "Promoters" not in result
    assert "Fraud" not in result


def test_entity_with_digits_is_rejected():
    text = "ISO 9001:2015"

    result = detect_person_names(text)

    assert "ISO 9001:2015" not in result


def test_email_like_entity_is_rejected():
    text = "Contact ksh.ipo@nuvama.com Website"

    result = detect_person_names(text)

    assert "ksh.ipo@nuvama.com Website" not in result


def test_business_terms_are_not_person_names():
    text = """
    Reference Rate
    Selling Shareholder
    Key Managerial Personnel
    """

    result = detect_person_names(text)

    assert "Reference Rate" not in result
    assert "Selling Shareholder" not in result
    assert "Key Managerial Personnel" not in result


def test_company_name_is_not_person_name():
    text = "Waterloo Industrial Park VI Private Limited"

    result = detect_person_names(text)

    assert "Waterloo Industrial Park VI Private Limited" not in result


def test_trust_name_is_not_person_name():
    text = "Dhaulagiri Family Trust"

    result = detect_person_names(text)

    assert "Dhaulagiri Family Trust" not in result


def test_person_with_middle_initial_is_detected():
    text = "Karunakar N. Bhandary"

    result = detect_person_names(text)

    assert "Karunakar N. Bhandary" in result


def test_normal_person_name_is_detected():
    text = "Kumar Tiwari is mentioned in the document."

    result = detect_person_names(text)

    assert "Kumar Tiwari" in result

def test_address_terms_are_not_person_names():
    text = """
    Bandra Kurla Complex
    Bandra East
    Chakan Taluka-Khed
    Model Colony
    """

    result = detect_person_names(text)

    assert "Bandra Kurla Complex" not in result
    assert "Bandra East" not in result
    assert "Chakan Taluka-Khed" not in result
    assert "Model Colony" not in result


def test_business_and_document_terms_are_not_person_names():
    text = """
    Bidder’s DP ID
    All Offer-related
    a Registered Broker
    corrigenda thereto
    """

    result = detect_person_names(text)

    assert "Bidder’s DP ID" not in result
    assert "All Offer-related" not in result
    assert "a Registered Broker" not in result
    assert "corrigenda thereto" not in result


def test_technical_terms_are_not_person_names():
    text = """
    Gram Jyoti DFI
    Mega Volt-Amperes
    Kisan Urja Suraksha
    Photo Voltaic
    """

    result = detect_person_names(text)

    assert "Gram Jyoti DFI" not in result
    assert "Mega Volt-Amperes" not in result
    assert "Kisan Urja Suraksha" not in result
    assert "Photo Voltaic" not in result


def test_huf_is_not_person_name():
    text = "Karunakar Hegde HUF"

    result = detect_person_names(text)

    assert "Karunakar Hegde HUF" not in result


def test_names_are_deduplicated_case_insensitively():
    text = """
    Kushal Subbayya Hegde
    KUSHAL SUBBAYYA HEGDE
    """

    result = detect_person_names(text)

    matching = [
        name
        for name in result
        if name.casefold() == "kushal subbayya hegde"
    ]

    assert len(matching) == 1

def test_remaining_document_artifacts_are_not_person_names():
    text = """
    Bidder’s DP ID
    All Offer-related
    WIDELY CIRCULATED MARATHI DAILY NEWSPAPER
    Chakan Taluka-Khed
    Kisan Urja Suraksha
    """

    result = detect_person_names(text)

    assert "Bidder’s DP ID" not in result
    assert "All Offer-related" not in result
    assert "WIDELY CIRCULATED MARATHI DAILY NEWSPAPER" not in result
    assert "Chakan Taluka-Khed" not in result
    assert "Kisan Urja Suraksha" not in result

def test_address_and_document_fragments_are_not_person_names():
    text = """
    Taluka Parner
    Taluka Khed
    Marg Backbay Reclamation Churchgate
    Sancheti Hospital Shivajinagar
    Waterloo Industrial Park IX
    Village Khalumbre
    Acknowledgement Slip
    Schedule XIII
    Description Red
    Nuvama S. No.
    """

    result = detect_person_names(text)

    assert "Taluka Parner" not in result
    assert "Taluka Khed" not in result
    assert "Marg Backbay Reclamation Churchgate" not in result
    assert "Sancheti Hospital Shivajinagar" not in result
    assert "Waterloo Industrial Park IX" not in result
    assert "Village Khalumbre" not in result
    assert "Acknowledgement Slip" not in result
    assert "Schedule XIII" not in result
    assert "Description Red" not in result
    assert "Nuvama S. No." not in result

def test_technical_fragments_are_not_person_names():
    text = """
    Gigawatt GWH
    Air Conditioning HVDC
    Mega Volt-Amperes
    Megawatt MWW
    """

    result = detect_person_names(text)

    assert "Gigawatt GWH" not in result
    assert "Air Conditioning HVDC" not in result
    assert "Mega Volt-Amperes" not in result
    assert "Megawatt MWW" not in result

def test_location_candidates_are_not_person_names():
    text = """
    Taluka Parner
    Taluka Khed
    Waterloo Industrial Park IX
    """

    result = detect_person_names(text)

    assert "Taluka Parner" not in result
    assert "Taluka Khed" not in result
    assert "Waterloo Industrial Park IX" not in result


def test_document_and_technical_candidates_are_not_person_names():
    text = """
    Schedule XIII
    Mega Volt-Amperes
    """

    result = detect_person_names(text)

    assert "Schedule XIII" not in result
    assert "Mega Volt-Amperes" not in result