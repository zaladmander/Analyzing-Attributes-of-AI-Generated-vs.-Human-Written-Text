from src.load_to_mysql import TABLE_NAME, get_connection
import mysql.connector
import pandas as pd

connection = get_connection()

def get_topic_data(topic):
    topicsSql = f"""
    select label, 
    case when label = 'human' then 'human'
    else source_detail
    end as source_group,
    AVG(length_chars) AS avg_chars,
    AVG(length_words) AS avg_words, 
    AVG(quality_score) AS avg_quality
    from {TABLE_NAME}
    where topic = '{topic}'
    group by label, source_group"""

    return pd.read_sql(topicsSql, connection)

topics = [
    "technology", "science", "sports", "health",
    "education", "lifestyle", "food", "travel",
    "finance", "entertainment"
]

topic_data = {}

for topic in topics:
    topic_data[topic] = get_topic_data(topic)

# for human vs ai
humanVsAiQuery = f"""
select label, 
AVG(length_chars) as avg_chars,
AVG(length_words) as avg_words, 
AVG(quality_score) as avg_quality
from {TABLE_NAME}
group by label"""

humanVsAiData = pd.read_sql(humanVsAiQuery, connection)
print(humanVsAiData)

# for within topics 
humanVsAiWithTopicsQuery = f"""
select label, topic,
AVG(length_chars) as avg_chars,
AVG(length_words) as avg_words, 
AVG(quality_score) as avg_quality
from {TABLE_NAME}
group by label, topic"""

humanVsAiWithTopicsData = pd.read_sql(humanVsAiWithTopicsQuery, connection)
print(humanVsAiWithTopicsData)

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
print(interAiData = pd.read_sql(interAiQuery, connection))