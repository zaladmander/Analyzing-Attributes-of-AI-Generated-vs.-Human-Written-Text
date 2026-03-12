from src.load_to_mysql import TABLE_NAME, get_connection
import mysql.connector
import pandas as pd

connection = get_connection()

textBySourceSql = f"""
select label, topic, 
AVG(length_chars) as avg_chars,
AVG(length_words) as avg_words, 
AVG(quality_score) as avg_quality
from {TABLE_NAME}
group by label, topic"""

textBySourceData = pd.read_sql(textBySourceSql, connection)

print(textBySourceData.head())