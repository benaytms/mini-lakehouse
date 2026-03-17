"""
    Gets the raw JSON file from the bucket bronze directory, parse it to be formatted
    Then converts into a parquet file into the silver directory.
"""

import pandas as pd
import io
import json
from bronze import BUCKET_NAME, ENDPOINT, REGION
from bronze import  make_connection, get_today


def get_json_from_s3(client, today):
    response = client.get_object(
        Bucket=BUCKET_NAME,
        Key=f'bronze/covid19/{today}.json'
        )
    return json.loads(response['Body'].read())


def parse_json(client, today):
    data = get_json_from_s3(client, today)

    df = pd.json_normalize(data, sep='.')

    columns_to_drop = ['updated', 'countryInfo._id']
    df = df.drop(columns_to_drop, axis=1)

    df = df.rename(columns={
        'countryInfo.iso2': 'iso2',
        'countryInfo.iso3': 'iso3',
        'countryInfo.lat': 'lat',
        'countryInfo.long': 'long',
        'countryInfo.flag': 'flag',
        'active': 'activePeople',
        'population': 'populationCount'
    })

    correct_dtypes: dict = {
        "country": "string",
        "cases": "Int64",
        "todayCases": "Int64",
        "deaths": "Int64",
        "todayDeaths": "Int64",
        "recovered": "Int64",
        "todayRecovered": "Int64", 
        "activePeople": "Int64",
        "critical": "Int64",
        "casesPerOneMillion": "Int64",
        "deathsPerOneMillion": "Int64",
        "tests": "Int64",
        "testsPerOneMillion": "Int64",
        "populationCount": "Int64",
        "continent": "string",
        "oneCasePerPeople": "Int64",
        "oneDeathPerPeople": "Int64",
        "oneTestPerPeople": "Int64",
        "activePerOneMillion": "float64",
        "recoveredPerOneMillion": "float64",
        "criticalPerOneMillion": "float64",
        "iso2": "string",
        "iso3": "string",
        "lat": "float64",
        "long": "float64",
        "flag": "string"
    }

    df = df.astype(correct_dtypes)
    return df


def send_silver(client):
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
    if send_silver(make_connection(ENDPOINT, REGION)):
        print(f"Success!")
    else:
        print(f"Something Went Wrong.")


