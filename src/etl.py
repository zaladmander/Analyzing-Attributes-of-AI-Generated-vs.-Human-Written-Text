import pandas as pd
from utils.paths import RAW_DATA_FILE, CLEAN_DATA_FILE, CLEAN_DATA

# just if you want to see some output while running the script
verbose = bool(int(input("Verbose output? (0 or 1): ")))

df = pd.read_csv(RAW_DATA_FILE)
if verbose:
    print("Raw data loaded from:", RAW_DATA_FILE)
    print(df.head())

df = (
    df
    .sort_values(by='id', ascending=True)
    .reset_index(drop=True)
)
if verbose:
    print("Data after sorting and resetting index:")
    print(df.head())

if verbose:
    print("Variables and their data types:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")

# make the clean directory under data if it doesn't exist
CLEAN_DATA.mkdir(parents=True, exist_ok=True)

# write to clean directory with a stable name, clean_data.csv
df.to_csv(CLEAN_DATA_FILE, index=False)
if verbose:
    print("Clean data written to:", CLEAN_DATA_FILE)