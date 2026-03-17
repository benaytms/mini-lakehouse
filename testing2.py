from pipeline.config import BUCKET_NAME, ENDPOINT, REGION
from pipeline.config import POSTGRES_URL
from pipeline.bronze import make_connection, get_today
import pandas as pd
import sqlalchemy
import io

def get_connection():
    return sqlalchemy.create_engine(POSTGRES_URL)

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
    df_countries = df[countries_table_cols]

    covid_cases_non_cols = ['country', 'continent', 'population_count', 'iso2', 'latitude', 'longitude', 'country_flag']
    df_covid_cases = df.drop(columns=covid_cases_non_cols)

    df_covid_cases['date'] = get_today()

    return (df_countries, df_covid_cases)


def add_dfs_to_tables():
    (df_countries, df_covid_cases) = separate_df(make_connection(ENDPOINT,REGION))

    

    df_countries.to_sql('countries', con=engine, if_exists='append', index=False)

    df_covid_cases.to_sql('covid_cases', con=engine, if_exists='append', index=False)

if __name__ == "__main__":

    pass



