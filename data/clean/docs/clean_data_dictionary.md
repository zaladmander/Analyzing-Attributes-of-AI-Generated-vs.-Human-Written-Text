# Clean Data — Data Dictionary

**Dataset:** data/clean/clean_data.csv

## Description

This document describes the columns present in `clean_data.csv`. It is intended to be human-readable documentation of variable meanings, units, allowed values, and any transformation notes. A machine-readable CSV companion is available at `docs/data_dictionary/clean_data_dictionary.csv`.

## Column reference

| Readable variable | Variable name | Type / measurement unit | Allowed values | Description |
|---|---:|---|---|---|
| id | id | int | unique | Primary key — unique row identifier |
| label | label | string | e.g. 'human', 'ai' | Origin label indicating whether text is human-written or AI-generated |
| topic | topic | string | n/a | Label indicating the topic that the text is talking about |
| text | text | string | n/a | Cleaned article body/text (lowercased, punctuation removed) |
| number of characters | length_chars | int | 60 - 300 | A value indicating the number of characters in the text |
| number of words | length_words | int | 8 - 50 | A value indicating the number of words in the text |
| quality score | quality_score | int | 1 - 5 | A value indicating how good the quality of the text is |
| sentiment score | sentiment | int | -1 - 1 | A value indicating how much sentiment and emotion is in the text |
| source | source_detail | string | e.g., 'human', 'claude-2' | Origin label indicating whether the text is written by a human author or the type of AI it came from |
| timestamp | timestamp | int | 2023-01-02 - 2025-09-24 | A timestamp of when the text was created |

## Notes

- `length_chars` and `length_words` are derived from the cleaned `text` column.
- All text preprocessing (lowercasing, punctuation removal) was applied before feature extraction.
- `quality_score` and `sentiment` may be manually annotated or generated using external models.
- `source_detail` provides more granular origin information than `label`.
- Ensure consistency between `label` and `source_detail` when analysing the data.

## Updating

- When new columns are added to `clean_data.csv`, they must also be documented in this data dictionary.
- Ensure that each new variable includes: name, type, allowed values, and a clear description.
- If transformations change (e.g., different preprocessing for `text`), update the corresponding notes to reflect this.
- If value ranges or categories change (e.g., new labels or sentiment scale), update the "Allowed values" column.
- Regenerate the machine-readable CSV (`clean_data_dictionary.csv`) if structural changes are made.
- Periodically review the dictionary to ensure consistency with the dataset.
