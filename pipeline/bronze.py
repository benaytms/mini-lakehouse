"""
    Fetches a JSON file with Covid-19 data from 2019
    Then sends to the bronze directory inside the bucket
"""

import requests as rq
import boto3 as b3
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from dotenv import load_dotenv
import os

load_dotenv()

BUCKET_NAME=str(os.getenv('BUCKET_NAME'))
ENDPOINT=str(os.getenv('ENDPOINT'))
REGION=str(os.getenv('REGIOIN'))
SOURCE_URL=str(os.getenv('SOURCE_URL'))


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
        print(f"Success!")
    else:
        print(f"Something Went Wrong")

