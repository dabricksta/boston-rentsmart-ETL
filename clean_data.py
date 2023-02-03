import pandas as pd
import json
from datetime import date, timedelta, datetime
import flatten_json
import csv
import os
import extract_data

# df = pd.DataFrame()

def open_json():
    # json_file = open(extract_data.extracted_data_fn, "r")
    with open(extract_data.extracted_data_fn) as json_file:
    # with open(f'rentsmart_json_2022-12-29.json') as json_file:
        # store file data in object
        json_data = json.load(json_file)
    print('json data loaded')
    print (json_data)
    df = pd.json_normalize(json_data['result']['records'])
    print ('raw json transformed to pandas DataFrame:\n', df.head(5))
    return df

def clean_data():
    #rename columns
    df = open_json()
    df = df.rename(columns = {'_id':'id', 'date':'datetime', 'year built':'year_built'
        , 'year remodeled':'year_remodeled'})
    #clean zip codes
    df['zip_code'] = df['zip_code'].apply(lambda x: '0' + str(x) if len(x) == 4 else str(x))
    #create date column from preexisting datetime
    df['date'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    df['date'] = df['date'].apply(lambda x: datetime.date(x))
    df['geo_coordinates'] = df['latitude'] + ', ' + df['longitude']
    #reorder
    df = df[['id', 'date', 'datetime', 'property_type', 'violation_type', 'description', 'owner', 'year_built'
        , 'year_remodeled', 'neighborhood', 'address', 'zip_code', 'parcel', 'geo_coordinates', 'latitude', 'longitude']]
    # df
    print('data transformation complete:\n', df.head(5))
    # return(dataframe)


# df = clean_data(df)
# df

# #################### checks in terminal ####################
# import pandas as pd
# import json
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# extracted_data_fn = f'rentsmart_json_2022-12-29.json'
# json_file = open(extracted_data_fn, "r")
# json_data = json.load(json_file)
# json_data['result']['fields'][0].keys()
# json_data
# df = pd.json_normalize(json_data['result']['records'])
# print(df)
# df = df.rename(columns = {'_id':'id', 'date':'datetime', 'year built':'year_built'
#         , 'year remodeled':'year_remodeled'})
# df['zip_code'] = df['zip_code'].apply(lambda x: '0' + str(x) if len(x) == 4 else str(x))
# df['date'] = df['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
# df['date'] = df['date'].apply(lambda x: datetime.datetime.date(x))
# df = df[['id', 'date', 'datetime', 'property_type', 'violation_type', 'description', 'owner', 'year_built'
#     , 'year_remodeled', 'neighborhood', 'address', 'zip_code', 'parcel', 'latitude', 'longitude']]
# df
# df.to_csv(f'rentsmart_flattened_data_2022-23-22.csv', index = False)
# df.to_csv(f'rentsmart_flattened_data_{yesterday}.csv', index=False)

# # column keys
