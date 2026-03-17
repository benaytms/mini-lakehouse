"""
    Gets the raw JSON file from the bucket bronze directory, parse it to be formatted
    Then converts into a parquet file into the silver directory.
"""

import pandas as pd
import io
import json
from pipeline.config import BUCKET_NAME, ENDPOINT, REGION
from pipeline.bronze import  make_connection, get_today


def get_json_from_s3(client, today:str):
    response = client.get_object(
        Bucket=BUCKET_NAME,
        Key=f'bronze/covid19/{today}.json'
        )
    return json.loads(response['Body'].read())


def parse_json(client, today:str)->pd.DataFrame:
    data = get_json_from_s3(client, today)

    df = pd.json_normalize(data, sep='.')

    columns_to_drop = ['updated', 'countryInfo._id']
    df = df.drop(columns_to_drop, axis=1)

    df = df.rename(columns={
        'countryInfo.iso2': 'iso2',
        'countryInfo.iso3': 'iso3',
        'countryInfo.lat': 'latitude',
        'countryInfo.long': 'longitude',
        'countryInfo.flag': 'country_flag',
        'active': 'active_people',
        'population': 'population_count',
        'todayCases': 'today_cases',
        'todayDeaths': 'today_deaths',
        'todayRecovered': 'today_recovered',
        'casesPerOneMillion': 'cases_per_one_million',
        'deathsPerOneMillion': 'deaths_per_one_million',
        'testsPerOneMillion': 'tests_per_one_million',
        'oneCasePerPeople': 'one_case_per_people',
        'oneDeathPerPeople': 'one_death_per_people',
        'oneTestPerPeople': 'one_test_per_people',
        'activePerOneMillion': 'active_per_one_million',
        'recoveredPerOneMillion': 'recovered_per_one_million',
        'criticalPerOneMillion': 'critical_per_one_million',
    })

    correct_dtypes: dict = {
        "country": "string",
        "cases": "Int64",
        "today_cases": "Int64",
        "deaths": "Int64",
        "today_deaths": "Int64",
        "recovered": "Int64",
        "today_recovered": "Int64",
        "active_people": "Int64",
        "critical": "Int64",
        "cases_per_one_million": "Int64",
        "deaths_per_one_million": "Int64",
        "tests": "Int64",
        "tests_per_one_million": "Int64",
        "population_count": "Int64",
        "continent": "string",
        "one_case_per_people": "Int64",
        "one_death_per_people": "Int64",
        "one_test_per_people": "Int64",
        "active_per_one_million": "float64",
        "recovered_per_one_million": "float64",
        "critical_per_one_million": "float64",
        "iso2": "string",
        "iso3": "string",
        "latitude": "float64",
        "longitude": "float64",
        "country_flag": "string"
    }
    df = df.astype(correct_dtypes)
    df = df.dropna(subset=['iso3'])         # guarantees won't have null primary keys
    return df


def silver_layer(client)->bool:
    today = get_today()
    df = parse_json(client, today)

    buffer = io.BytesIO()
    df.to_parquet(buffer, index=True)

    key = f'silver/covid19/{today}.parquet'

    for attempt in range(1,6):
        try:
            buffer.seek(0)
            print(f"Adding object to S3, attempt {attempt}")
            client.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=buffer.getvalue()
            )
            print(f"Succesfully added new file: {key}")
            return True
        except Exception as e:
            print(f"An Error occurred: {e}")
            if attempt==5:
                raise
    return False


if __name__ == "__main__":
    if silver_layer(make_connection(ENDPOINT, REGION)):
        print("Silver layer successfully executed!")
    else:
        print("Something Went Wrong in the Silver Phase")


