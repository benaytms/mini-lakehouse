"""
    Fetches a JSON file with Covid-19 data from 2019
    Then sends to the bronze directory inside the bucket
"""

from pipeline.config import BUCKET_NAME, ENDPOINT, REGION, SOURCE_URL
from datetime import datetime
from zoneinfo import ZoneInfo
import requests as rq
import boto3 as b3
import json


def make_connection(ENDPOINT,REGION):
    try:
        client = b3.client(
            's3',
            endpoint_url=ENDPOINT,
            aws_access_key_id='fake',
            aws_secret_access_key='fake',
            region_name=REGION
        )
    except Exception as e:
        print(f"An Error occurred: {e}")
        raise
    return client


def get_today()->str:
    return datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat()


def fetch_bronze(client)->bool:
    today = get_today()
    key = f'bronze/covid19/{today}.json'
    for attempt in range(1,6):
        try:
            print(f"Fetching bronze files. Attempt No. {attempt}: ")
            response = rq.get(SOURCE_URL)
            response.raise_for_status()

            data = response.json()
            client.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=json.dumps(data)
            )
            print(f"Succesfully fetched data: {key}")
            return True
        except Exception as e:
            print(f"An Error occurred: {e}")
            if attempt==5:
                raise
    return False

if __name__ == '__main__':
    if fetch_bronze(make_connection(ENDPOINT,REGION)):
        print("Bronze layer successfully executed!")
    else:
        print("Something Went Wrong in the Bronze Phase")

