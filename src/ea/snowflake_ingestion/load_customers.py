import snowflake.connector
import pandas as pd
import numpy as np
from dotenv import dotenv_values
from loguru import logger

config = dotenv_values('.env')

SNOWFLAKE_USER = config.get("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = config.get("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = config.get("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = config.get("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = config.get("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = config.get("SNOWFLAKE_SCHEMA")


def load_customers(file_path):
    logger.info("Connecting to Snowflake...")

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

    cur = conn.cursor()

    logger.info("Creating bronze.customers table if not exists...")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bronze.customers (
        customer_id STRING,
        first_name STRING,
        last_name STRING,
        age INTEGER,
        contact_pref STRING,
        vehicle_id INTEGER
    )
    """)

    logger.info(f"Reading file: {file_path}")
    df = pd.read_csv(file_path)

    # Replace all NaNs with None (works for numeric and object columns)
    df = df.replace({np.nan: None})

    logger.info(f"Inserting {len(df)} records into Snowflake...")

    data = [tuple(row) for _, row in df.iterrows()]

    cur.executemany("""
        INSERT INTO bronze.customers (
            customer_id, first_name, last_name, age, contact_pref, vehicle_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, data)

    conn.commit()
    logger.info("Load complete ✅")

    cur.close()
    conn.close()