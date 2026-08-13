import json
import sys
from pathlib import Path
from collections import defaultdict


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.document_reader import read_docx
from src.detectors import (
    detect_person_names,
    detect_emails,
    detect_phone_numbers,
    detect_company_names,
    detect_ssns,
    detect_credit_cards,
    detect_dates_of_birth,
    detect_ip_addresses,
)


INPUT_FILE = PROJECT_ROOT / "input" / "Red Herring Prospectus.docx"
GOLD_FILE = PROJECT_ROOT / "evaluation" / "gold_annotations.json"


DETECTORS = {
    "PERSON": detect_person_names,
    "EMAIL": detect_emails,
    "PHONE": detect_phone_numbers,
    "COMPANY": detect_company_names,
    "SSN": detect_ssns,
    "CREDIT_CARD": detect_credit_cards,
    "DOB": detect_dates_of_birth,
    "IP_ADDRESS": detect_ip_addresses,
}


def normalize(value: str) -> str:
    """Normalize text for case-insensitive exact matching."""
    return " ".join(value.split()).casefold()


def load_gold_annotations() -> list[dict]:
    """Load manually verified annotations."""
    with GOLD_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data["annotations"]


def group_gold_by_type(
    annotations: list[dict],
) -> dict[str, set[str]]:
    """Group gold annotations by PII type."""
    grouped = defaultdict(set)

    for annotation in annotations:
        grouped[annotation["type"]].add(
            normalize(annotation["text"])
        )

    return dict(grouped)


def calculate_metrics(
    gold: set[str],
    predictions: set[str],
) -> dict[str, float | int]:
    """Calculate TP, FP, FN, precision, recall and F1."""

    true_positive = len(gold & predictions)
    false_positive = len(predictions - gold)
    false_negative = len(gold - predictions)

    if true_positive + false_positive:
        precision = (
            true_positive
            / (true_positive + false_positive)
        )
    else:
        precision = 0.0

    if true_positive + false_negative:
        recall = (
            true_positive
            / (true_positive + false_negative)
        )
    else:
        recall = 0.0

    if precision + recall:
        f1 = (
            2 * precision * recall
            / (precision + recall)
        )
    else:
        f1 = 0.0

    return {
        "tp": true_positive,
        "fp": false_positive,
        "fn": false_negative,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def run_evaluation() -> dict[str, dict]:
    """Run every detector against the gold annotations."""

    print("Reading prospectus...")

    text = read_docx(INPUT_FILE)

    print(f"Characters loaded: {len(text)}")
    print()

    annotations = load_gold_annotations()

    gold_by_type = group_gold_by_type(
        annotations
    )

    results = {}

    for pii_type, detector in DETECTORS.items():

        print(
            f"Running {pii_type} detector..."
        )

        # -----------------------------------------------------
        # COMPANY:
        # Use the optional assignment-specific filter.
        #
        # All other detectors use their normal interface.
        # -----------------------------------------------------

        if pii_type == "COMPANY":
            detected = detector(
                text,
                allowed_only=True,
            )
        else:
            detected = detector(text)

        # -----------------------------------------------------
        # Normalize predictions
        # -----------------------------------------------------

        predictions = {
            normalize(value)
            for value in detected
        }

        # -----------------------------------------------------
        # Get gold annotations
        # -----------------------------------------------------

        gold = gold_by_type.get(
            pii_type,
            set(),
        )

        # -----------------------------------------------------
        # Calculate metrics
        # -----------------------------------------------------

        metrics = calculate_metrics(
            gold=gold,
            predictions=predictions,
        )

        results[pii_type] = metrics

        # -----------------------------------------------------
        # Print metrics
        # -----------------------------------------------------

        print(
            f"  Gold instances : "
            f"{len(gold)}"
        )

        print(
            f"  Predictions    : "
            f"{len(predictions)}"
        )

        print(
            f"  TP             : "
            f"{metrics['tp']}"
        )

        print(
            f"  FP             : "
            f"{metrics['fp']}"
        )

        print(
            f"  FN             : "
            f"{metrics['fn']}"
        )

        print(
            f"  Precision      : "
            f"{metrics['precision']:.4f}"
        )

        print(
            f"  Recall         : "
            f"{metrics['recall']:.4f}"
        )

        print(
            f"  F1             : "
            f"{metrics['f1']:.4f}"
        )

        print()

    return results


def main() -> None:
    """Run evaluation and print the final summary."""

    results = run_evaluation()

    print("=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    for pii_type, metrics in results.items():

        print(
            f"{pii_type:15} "
            f"Precision={metrics['precision']:.4f} "
            f"Recall={metrics['recall']:.4f} "
            f"F1={metrics['f1']:.4f}"
        )


if __name__ == "__main__":
    main()