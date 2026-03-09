import kagglehub
from utils.paths import RAW_DATA

RAW_DATA.mkdir(parents=True, exist_ok=True)

# Download latest version
path = kagglehub.dataset_download(
    "prince7489/ai-vs-human-comparison-dataset", 
    output_dir=str(RAW_DATA),
)

print("Path to raw data:", path)