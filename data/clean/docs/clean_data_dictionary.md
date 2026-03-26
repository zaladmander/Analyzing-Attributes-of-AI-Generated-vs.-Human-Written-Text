# Clean Data — Data Dictionary

**Dataset:** data/clean/clean_data.csv
**Generated on:** 2026-03-17

## Description

This document describes the columns present in `clean_data.csv`. It is intended to be human-readable documentation of variable meanings, units, allowed values, and any transformation notes. A machine-readable CSV companion is available at `docs/data_dictionary/clean_data_dictionary.csv`.

## Column reference

| Readable variable | Variable name | Type / measurement unit | Allowed values | Description |
|---|---:|---|---|---|
| id | id | int | unique | Primary key — unique row identifier |
| text | text | string | n/a | Cleaned article body/text (lowercased, punctuation removed) |
| source | source | string | e.g., 'human', 'gpt' | Origin label indicating whether text is human-written or AI-generated |

## Notes

- Fill in or extend rows above with dataset-specific columns.
- For derived variables, include the transformation in the description or in the `notes` field of the CSV.

## Updating

- You can auto-generate a starter CSV of column metadata then edit it manually to add descriptions and allowed values.
