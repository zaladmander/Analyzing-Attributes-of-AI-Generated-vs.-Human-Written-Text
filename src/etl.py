import pandas as pd
from utils.paths import RAW_DATA_FILE

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