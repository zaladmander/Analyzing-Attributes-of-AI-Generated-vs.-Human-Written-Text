from src.load_to_mysql import TABLE_NAME, get_connection 
import mysql.connector
import pandas as pd
import os

connection = get_connection()

# for human vs ai
humanVsAiQuery = f"""
select label, 
AVG(length_chars) as avg_chars,
AVG(length_words) as avg_words, 
AVG(quality_score) as avg_quality
from {TABLE_NAME}
group by label"""

humanVsAiData = pd.read_sql(humanVsAiQuery, connection)

# for within topics 
humanVsAiWithTopicsQuery = f"""
select label, topic,
AVG(length_chars) as avg_chars,
AVG(length_words) as avg_words, 
AVG(quality_score) as avg_quality
from {TABLE_NAME}
group by label, topic"""

humanVsAiWithTopicsData = pd.read_sql(humanVsAiWithTopicsQuery, connection)

# for inter-ai analysis
interAiQuery = f"""
select label, source_detail,
AVG(length_chars) as avg_chars,
AVG(length_words) as avg_words, 
AVG(quality_score) as avg_quality
from {TABLE_NAME}
where not label = 'human'
group by label, source_detail"""

interAiData = pd.read_sql(interAiQuery, connection)

# export to csv
os.makedirs("Cleaned Data CSVs/text_complexity/", exist_ok=True)

humanVsAiData.to_csv("Cleaned Data CSVs/text_complexity/human_vs_ai_text_complexity.csv", index=False)
humanVsAiWithTopicsData.to_csv("Cleaned Data CSVs/text_complexity/human_vs_ai_topics_text_complexity.csv", index=False)
interAiData.to_csv("Cleaned Data CSVs/text_complexity/inter_ai_text_complexity.csv", index=False)
print(f"\nWrote data to csv files.")

connection.close()