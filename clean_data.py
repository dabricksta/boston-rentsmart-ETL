import pandas as pd
import json
from datetime import date, timedelta, datetime
import flatten_json
import csv
import os
import extract_data

# yesterday = date.today() - timedelta(days = 1)
# extracted_data_fn = f'rentsmart_json_{yesterday}.json'

# with open(extracted_data_fn) as json_file:
with open('rentsmart_json_2022-11-23.json') as json_file:
    # store file data in object
    json_data = json.load(json_file)
    print (json_data)
    df = pd.json_normalize(json_data['result']['records'])
    print (df)


def clean_data(dataframe):
    #rename columns
    dataframe = dataframe.rename(columns = {'_id':'id', 'date':'datetime', 'year built':'year_built'
        , 'year remodeled':'year_remodeled'})
    #clean zip codes
    dataframe['zip_code'] = dataframe['zip_code'].apply(lambda x: '0' + str(x) if len(x) == 4 else str(x))
    #create date column from preexisting datetime
    dataframe['date'] = dataframe['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    dataframe['date'] = dataframe['date'].apply(lambda x: datetime.datetime.date(x))
    dataframe['geo_coordinates'] = dataframe['latitude'] + ', ' + dataframe['longitude']
    #reorder
    dataframe = dataframe[['id', 'date', 'datetime', 'property_type', 'violation_type', 'description', 'owner', 'year_built'
        , 'year_remodeled', 'neighborhood', 'address', 'zip_code', 'parcel', 'geo_coordinates', 'latitude', 'longitude']]
    # dataframe
    return(dataframe)


# df = clean_data(df)
# df

#################### checks in terminal ####################

# df = pd.json_normalize(json_data['result']['records'])
# df
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

# column keys
