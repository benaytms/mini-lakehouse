#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests as rq
import pandas as pd
import io
import boto3 as b3

pd.set_option('display.max_columns', None)


# In[2]:


try:
    response = rq.get("https://disease.sh/v3/covid-19/countries")
except Exception as e:
    print(f"Error occurred: {e}")
    raise


# In[3]:


data = response.json()


# In[4]:


to_flatten=[]
for i in data[0]:
    datatype=type(data[0][i])
    print(datatype)
    if datatype is dict:
        to_flatten.append(i)


# In[5]:


to_flatten


# In[6]:


data[0]['countryInfo']


# In[7]:


df = pd.json_normalize(data, sep='.')


# In[8]:


df.head(2)


# In[9]:


columns_to_drop = ['updated', 'countryInfo._id']
df = df.drop(columns_to_drop, axis=1)


# In[10]:


df = df.set_index('country')


# In[11]:


df = df.rename(columns={
    'countryInfo.iso2': 'iso2',
    'countryInfo.iso3': 'iso3',
    'countryInfo.lat': 'lat',
    'countryInfo.long': 'long',
    'countryInfo.flag': 'flag'
})


# In[12]:


df.loc[['Chile', 'Brazil']]


# In[13]:


correct_dtypes: dict = {
    "cases": "Int64",
    "todayCases": "Int64",
    "deaths": "Int64",
    "todayDeaths": "Int64",
    "recovered": "Int64",
    "todayRecovered": "Int64", 
    "active": "Int64",
    "critical": "Int64",
    "casesPerOneMillion": "Int64",
    "deathsPerOneMillion": "Int64",
    "tests": "Int64",
    "testsPerOneMillion": "Int64",
    "population": "Int64",
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


# In[14]:


df = df.astype(correct_dtypes)


# In[15]:


df.dtypes


# In[16]:


buffer = io.BytesIO()
df.to_parquet(buffer, index=True)
buffer.seek(0)


# In[17]:


BUCKET_NAME='mini-lakehouse-benaytms-bucket'
ENDPOINT='http://localhost:4566'
REGION='sa-east-1'
SOURCE_URL="https://disease.sh/v3/covid-19/countries"

client = b3.client(
    's3',
    endpoint_url=ENDPOINT,
    aws_access_key_id='fake',
    aws_secret_access_key='fake',
    region_name=REGION
)


# In[18]:


client.put_object(
    Bucket=BUCKET_NAME,
    Key='silver/covid19/2026-03-17.parquet',
    Body=buffer.getvalue()
)


# In[ ]:




