import json
import requests
import configparser
import datetime
import pandas as pd
import pathlib
import sys
import numpy as np
import boto3
# import validate_input
from datetime import date, timedelta


"""
Part of Airflow DAG. Takes 1 input of AWS S3 bucket name. 
Script will connect to Boston RentSmart API endpoint and extract data from
the past 24 hours then save raw JSON locally.
"""

# Read Configuration File
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.resolve()
config_file = "configuration.conf"
parser.read(f"{script_path}/{config_file}")

yesterday = date.today() - timedelta(days = 1)
extracted_data_fn = f'rentsmart_json_{yesterday}.json'
data_url = f'https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22dc615ff7-2ff3-416a-922b-f0f334f085d0%22%20where%20date%20%3E=%20%27{yesterday}%27' 

def main():
    """Extract data from the Boston RentSmart API"""
    call_boston_gov_api()
    upload_to_s3('boston-rent-smart-data-ddbr')

def call_boston_gov_api (url = data_url, file_name = extracted_data_fn):
    print('begin extraction')
    response = requests.request('GET', url)
    json_data = response.json()
    # print the first 5 items in the json response dict
    print('json response received \n')
    print(list(json_data.items())[:5])

    with open(file_name, 'w', encoding = 'utf-8') as json_file:
        json.dump(json_data, fp = json_file, ensure_ascii = False, indent = 4)
    print ('raw json data saved at:', file_name, '\n end running')

def upload_to_s3(bucket, file_name = extracted_data_fn):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, f"{bucket}/{file_name}")

if __name__ == '__main__':
    main()
