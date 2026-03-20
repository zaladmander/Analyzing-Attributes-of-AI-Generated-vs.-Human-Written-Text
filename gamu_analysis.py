import numpy as np
import pandas as pd
import mysql.connector
import os
import nltk
from scipy import stats

nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize, word_tokenize

DB_CONFIG = {
    "user":     os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "rootpassword"),
    "host":     os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port":     int(os.getenv("MYSQL_PORT", "3367")),
    "database": os.getenv("MYSQL_DATABASE", "clean_data"),
}


# Open a connection, pull only the columns we need, then close immediately
# to avoid holding the connection open during the slow NLP processing below
conn = mysql.connector.connect(**DB_CONFIG)
df = pd.read_sql("SELECT id, text, label, source_detail FROM clean_data", conn)
conn.close()


def type_token_ratio(text: str) -> float | None:
    # Lowercase and tokenize into individual words, stripping punctuation
    words = [w for w in word_tokenize(text.lower()) if w.isalpha()]

    # Skip texts shorter than 10 words — TTR is misleadingly high on short
    # texts (e.g. a 3-word text is 100% unique by default), which would skew
    # our comparison between AI and human writing
    if len(words) < 10:
        return None

    # TTR = unique words / total words
    # Higher TTR → more varied vocabulary
    # Lower TTR → more repetition (expected in AI writing)
    return len(set(words)) / len(words)

def sentence_length_std(text: str) -> float | None:
    # Split text into individual sentences using NLTK's sentence tokenizer
    sentences = sent_tokenize(text)

    # Need at least 2 sentences to measure variance — std of a single value
    # is always 0 and would pollute the results
    if len(sentences) < 2:
        return None

    # Count words per sentence, then take the standard deviation across all
    # sentences in this text.
    # Higher std → sentence lengths jump around a lot (expected in humans)
    # Lower std → sentences are more uniform in length (expected in AI)
    return float(np.std([len(word_tokenize(s)) for s in sentences]))

# Apply features to every row
# Rows that don't meet the minimums above will get None (stored as NaN)
df["ttr"]          = df["text"].apply(type_token_ratio)
df["sent_len_std"] = df["text"].apply(sentence_length_std)


# Compute mean, median, and std of both metrics broken down by label (AI vs human)
summary = (
    df.groupby("label")[["ttr", "sent_len_std"]]
    .agg(["mean", "median", "std"])
    .round(4)
)
print("\n=== Summary by label ===")
print(summary)

# Mann-Whitney U tests 
# Split into two groups for statistical testing
human_df = df[df["label"] == "human"]
ai_df    = df[df["label"] == "ai"]

# Mann-Whitney U is a non-parametric test — it doesn't assume a normal
# distribution, which is important here since text length distributions are
# typically skewed. It tests whether one group's values tend to be higher
# than the other's. p < 0.05 means the difference is statistically significant
# and unlikely to be due to chance.
for metric, label in [("sent_len_std", "Sentence length std"), ("ttr", "TTR")]:
    human_vals = human_df[metric].dropna()
    ai_vals    = ai_df[metric].dropna()
    stat, p    = stats.mannwhitneyu(human_vals, ai_vals, alternative="two-sided")
    print(f"\n{label}: U={stat:.1f}, p={p:.4f} {'✓ significant' if p < 0.05 else '✗ not significant'}")

# Write results back to MySQL for Power BI
results_df = df[["id", "label", "source_detail", "ttr", "sent_len_std"]].copy()

conn   = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS gamu_analysis (
        id            INT PRIMARY KEY,
        label         TEXT,
        source_detail TEXT,
        ttr           DOUBLE NULL,
        sent_len_std  DOUBLE NULL
    )
""")

# Wipe any previous run's results so we don't accumulate duplicate rows
cursor.execute("TRUNCATE TABLE gamu_analysis")

# Convert NaN → None so mysql.connector stores them as SQL NULL rather than
# trying to insert the Python float NaN, which would throw an error
rows = [
    tuple(None if pd.isna(v) else v for v in row)
    for row in results_df.itertuples(index=False, name=None)
]
cursor.executemany(
    "INSERT INTO gamu_analysis (id, label, source_detail, ttr, sent_len_std) VALUES (%s, %s, %s, %s, %s)",
    rows
)
conn.commit()
cursor.close()
conn.close()

print(f"\nWrote {len(results_df)} rows to gamu_analysis table.")