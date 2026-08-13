import json

from src.document_reader import read_docx
from src.detectors import detect_company_names


# Use the SAME prospectus path used by your evaluation scripts.
PROSPECTUS_PATH = "YOUR_CORRECT_PROSPECTUS_PATH_HERE"
GOLD_PATH = "evaluation/gold_annotations.json"


with open(GOLD_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

gold = [
    item["text"]
    for item in data["annotations"]
    if item["type"] == "COMPANY"
]

text = read_docx(PROSPECTUS_PATH)
predictions = detect_company_names(text)

prediction_keys = {
    company.casefold()
    for company in predictions
}

print("MISSING COMPANY NAMES")
print("=" * 60)

missing = [
    company
    for company in gold
    if company.casefold() not in prediction_keys
]

for company in missing:
    print(company)

print()
print(f"Gold companies      : {len(gold)}")
print(f"Predicted companies : {len(predictions)}")
print(f"Missing             : {len(missing)}")