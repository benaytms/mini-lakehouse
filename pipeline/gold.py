"""
    Extract the parquet from the silver directory
    And parses it into a PostgreSQL table
"""

from pipeline.config import BUCKET_NAME, ENDPOINT, REGION
from pipeline.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, HOST, PORT
from pipeline.bronze import make_connection, get_today
import pandas as pd
import psycopg2
import io

def get_connection():
    return psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def get_parquet_as_df(client):
    today=get_today()
    response = client.get_object(
        Bucket=BUCKET_NAME,
        Key=f'silver/covid19/{today}.parquet'
    )
    return pd.read_parquet(io.BytesIO(response['Body'].read()))

def separate_df(client):
    df = get_parquet_as_df(client)
    countries_table_cols = ['iso3', 'country', 'continent', 'population_count', 'iso2', 'latitude', 'longitude', 'country_flag']
    covid_cases_non_cols = ['country', 'continent', 'population_count', 'iso2', 'latitude', 'longitude', 'country_flag']

    df_countries = df[countries_table_cols]
    df_covid_cases = df.drop(columns=covid_cases_non_cols)
    df_covid_cases = df_covid_cases.copy()
    df_covid_cases['date'] = get_today()

    return (df_countries, df_covid_cases)

def upsert_df(df:pd.DataFrame, table_name:str, conflict_cols:list[str]):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cols = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            conflict = ', '.join(conflict_cols)
            sql = f"""
                INSERT INTO {table_name} ({cols})
                VALUES ({placeholders})
                ON CONFLICT ({conflict}) DO NOTHING
            """
            cur.executemany(sql, df.values.tolist())
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

def gold_layer(client)->bool:
    try:
        (df_countries, df_covid_cases) = separate_df(client)

        upsert_df(df_countries, 'countries', ['iso3'])
        print("Succesfully added countries")
        upsert_df(df_covid_cases, 'covid_cases', ['iso3', 'date'])
        print("Succesfully added covid_cases")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    if gold_layer(make_connection(ENDPOINT, REGION)):
        print("Gold layer successfully executed!")
    else:
        print("Something Went Wrong in the Gold Phase")
