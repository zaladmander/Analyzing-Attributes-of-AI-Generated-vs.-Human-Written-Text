#!/usr/bin/env python3
"""Generate a starter data dictionary CSV using the project's path helper.

This script imports `src/utils/paths.py` to locate `clean_data.csv` and
writes a data dictionary to `src/data_dictionary/clean_data_dictionary.csv`.
"""
import csv
import sys
from utils.paths import CLEAN_DATA, CLEAN_DATA_FILE

# We will only write the data dictionary into the data folder docs so it
# remains colocated with the data while data files remain gitignored.
CLEAN_DOCS_DIR = CLEAN_DATA / "docs"
CLEAN_DOCS_FILE = CLEAN_DOCS_DIR / "clean_data_dictionary.csv"

def main():
    if not CLEAN_DATA_FILE.exists():
        print(f"Input file not found: {CLEAN_DATA_FILE}")
        sys.exit(2)

    # Build rows
    rows = [
        {"readable_var": "ID", "var_name": "id", "type": "int64", "allowed_values": "", "description": "Unique row identifier"},
        {"readable_var": "Label (AI or Human)", "var_name": "label", "type": "str", "allowed_values": "", "description": "Categorical label"},
        {"readable_var": "Topic of Text", "var_name": "topic", "type": "str", "allowed_values": "", "description": "Topic or category of the text"},
        {"readable_var": "Text", "var_name": "text", "type": "str", "allowed_values": "", "description": "Main article or passage text"},
        {"readable_var": "Length of Text in Characters", "var_name": "length_chars", "type": "int64", "allowed_values": "", "description": "Character length of text"},
        {"readable_var": "Length of Text in Words", "var_name": "length_words", "type": "int64", "allowed_values": "", "description": "Word count of text"},
        {"readable_var": "Quality Score of Text", "var_name": "quality_score", "type": "float64", "allowed_values": "", "description": "Human or automatic quality rating"},
        {"readable_var": "Sentiment", "var_name": "sentiment", "type": "float64", "allowed_values": "", "description": "Sentiment score (e.g., -1 to 1)"},
        {"readable_var": "Source Detail", "var_name": "source_detail", "type": "str", "allowed_values": "", "description": "More granular source information"},
        {"readable_var": "Timestamp", "var_name": "timestamp", "type": "str", "allowed_values": "", "description": "ISO timestamp or original date string"},
        {"readable_var": "Plagiarism Score", "var_name": "plagiarism_score", "type": "float64", "allowed_values": "", "description": "Estimated similarity/plagiarism score"},
        {"readable_var": "Notes about Text", "var_name": "notes", "type": "str", "allowed_values": "", "description": "Freeform notes or flags"},
    ]

    fieldnames = ["readable_var", "var_name", "type", "allowed_values", "description"]

    # Ensure the target data docs directory exists and write just there.
    CLEAN_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    with open(CLEAN_DOCS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Wrote data dictionary to {CLEAN_DOCS_FILE}")


if __name__ == "__main__":
    main()
