import os
import time
from typing import Any

import mysql.connector
import pandas as pd
from mysql.connector import errorcode

from utils.paths import CLEAN_DATA_FILE

DB_CONFIG = {
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "rootpassword"),
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3367")),
    "database": os.getenv("MYSQL_DATABASE", "clean_data"),
}

TABLE_NAME = "clean_data"
MAX_RETRIES = 12
RETRY_DELAY_SECONDS = 5


def get_connection() -> Any:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as err:
            if attempt == MAX_RETRIES:
                raise err
            print(
                f"MySQL not ready yet ({err}). "
                f"Retrying in {RETRY_DELAY_SECONDS} seconds... "
                f"[{attempt}/{MAX_RETRIES}]"
            )
            time.sleep(RETRY_DELAY_SECONDS)

    raise RuntimeError("Unable to establish a MySQL connection.")


def mysql_type_for_series(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "INT"
    if pd.api.types.is_float_dtype(series):
        return "DOUBLE"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "DATETIME"
    return "TEXT"


def build_create_table_sql(df: pd.DataFrame) -> str:
    column_definitions = []
    for column_name in df.columns:
        sql_type = mysql_type_for_series(df[column_name])
        nullability = "NOT NULL" if df[column_name].notna().all() else "NULL"
        if column_name == "id":
            column_definitions.append(f"`{column_name}` {sql_type} NOT NULL")
        else:
            column_definitions.append(f"`{column_name}` {sql_type} {nullability}")

    column_definitions.append("PRIMARY KEY (`id`)")
    formatted_columns = ",\n        ".join(column_definitions)

    return f"""
    CREATE TABLE `{TABLE_NAME}` (
        {formatted_columns}
    )
    """.strip()


def prepare_dataframe() -> pd.DataFrame:
    df = pd.read_csv(CLEAN_DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def load_csv_to_mysql() -> None:
    df = prepare_dataframe()
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(f"DROP TABLE IF EXISTS `{TABLE_NAME}`")
        cursor.execute(build_create_table_sql(df))

        columns_sql = ", ".join(f"`{column}`" for column in df.columns)
        placeholders_sql = ", ".join(["%s"] * len(df.columns))
        insert_sql = (
            f"INSERT INTO `{TABLE_NAME}` ({columns_sql}) "
            f"VALUES ({placeholders_sql})"
        )

        rows = [
            tuple(None if pd.isna(value) else value for value in row)
            for row in df.itertuples(index=False, name=None)
        ]
        cursor.executemany(insert_sql, rows)
        connection.commit()

        print(
            f"Loaded {len(df)} rows from {CLEAN_DATA_FILE.name} "
            f"into {DB_CONFIG['database']}.{TABLE_NAME}."
        )
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    try:
        load_csv_to_mysql()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise