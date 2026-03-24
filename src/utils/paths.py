from pathlib import Path

# all of this really only works if nobody moves stuff around

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA = DATA_DIR / "raw"
CLEAN_DATA = DATA_DIR / "clean"

RAW_DATA_FILE = RAW_DATA / "raw_data.csv"
CLEAN_DATA_FILE = CLEAN_DATA / "clean_data.csv"