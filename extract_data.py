import json
import requests
from datetime import date

data_url = 'https://data.boston.gov/api/3/action/datastore_search?resource_id=ecb8e8a6-b5cf-41ea-8cbe-73fd53e03219&limit=5&q=title:jones'  

def json_scraper(url, file_name, bucket):
    print('begin execution')
    response = requests.request('GET', url)
    json_data = response.json()

    with open(file_name, 'w', encoding = 'utf-8') as json_file:
        json.dump(json_data, fp = json_file, ensure_ascii = False, indent = 4)
    print (file_name)
    print ('end running')
    # s3 = boto3.client('s3')
    # s3.upload_file(file_name, bucket, f"boston-rent-smart-data-ddbr/{file_name}")

json_scraper(data_url, f'rentsmart_json_{date.today()}.json', 'boston-rent-smart-data-ddbr')
import json
import urllib.request
url = 'https://data.boston.gov/api/3/action/datastore_search?resource_id=dc615ff7-2ff3-416a-922b-f0f334f085d0&limit=5&q=title:jones'  
fileobj = urllib.request.urlopen(url)
response_dict = json.loads(fileobj.read())
print(response_dict)