from dotenv import load_dotenv
import os

load_dotenv()

BUCKET_NAME=str(os.getenv('BUCKET_NAME'))
ENDPOINT=str(os.getenv('ENDPOINT'))
REGION=str(os.getenv('REGIOIN'))
SOURCE_URL=str(os.getenv('SOURCE_URL'))
DB_SYSTEM=str(os.getenv('DB_SYSTEM'))
#DB_DIALECT=str(os.getenv('DB_DIALECT'))
POSTGRES_USER=str(os.getenv('POSTGRES_USER'))
POSTGRES_PASSWORD=str(os.getenv('POSTGRES_PASSWORD'))
POSTGRES_DB=str(os.getenv('POSTGRES_DB'))
HOST=str(os.getenv('HOST'))
PORT=str(os.getenv('PORT'))
#POSTGRES_URL=f'{DB_SYSTEM}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{POSTGRES_DB}'