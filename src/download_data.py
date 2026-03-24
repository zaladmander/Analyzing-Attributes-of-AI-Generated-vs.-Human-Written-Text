import kagglehub
from pathlib import Path
from utils.paths import RAW_DATA, RAW_DATA_FILE

RAW_DATA.mkdir(parents=True, exist_ok=True)

# Download latest version
path = kagglehub.dataset_download(
    "prince7489/ai-vs-human-comparison-dataset", 
    output_dir=str(RAW_DATA),
    force_download=True
)

# find downloaded csv(s)
csv_files = list(RAW_DATA.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV file found in raw data directory after download.")

if len(csv_files) > 1:
    raise RuntimeError(f"Expected 1 CSV file, found {len(csv_files)}: {csv_files}")

downloaded_csv = csv_files[0]

# rename to a stable internal name
if downloaded_csv != RAW_DATA_FILE:
    downloaded_csv.replace(RAW_DATA_FILE)

print("Path to raw data:", RAW_DATA_FILE)