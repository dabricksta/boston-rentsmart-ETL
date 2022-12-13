import json
import requests
from datetime import date, timedelta

yesterday = date.today() - timedelta(days = 1)
extracted_data_fn = f'rentsmart_json_{yesterday}.json'
data_url = f'https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22dc615ff7-2ff3-416a-922b-f0f334f085d0%22%20where%20date%20%3E=%20%27{yesterday}%27' 

def call_boston_gov_api (url, file_name, bucket):
    print('begin execution')
    response = requests.request('GET', url)
    json_data = response.json()
    print(json_data)

    with open(file_name, 'w', encoding = 'utf-8') as json_file:
        json.dump(json_data, fp = json_file, ensure_ascii = False, indent = 4)
    print (file_name)
    print ('end running')
    # s3 = boto3.client('s3')
    # s3.upload_file(file_name, bucket, f"boston-rent-smart-data-ddbr/{file_name}")

# call_boston_gov_api(data_url, extracted_data_fn, 'boston-rent-smart-data-ddbr')

