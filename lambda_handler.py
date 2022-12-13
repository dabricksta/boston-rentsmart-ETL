import json
import boto3
import pandas as pd
from io import StringIO # python3; python2: BytesIO 


def lambda_handler(event, context):
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
 
    bucket = 'covid19autoupdate' # already created on S3
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, 'df.csv').put(Body=csv_buffer.getvalue())
