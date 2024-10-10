import datetime
from io import BytesIO, StringIO
import boto3
import pandas as pd

s3 = boto3.client('s3', region_name='eu-west-2')

class AWSTools:

    "Static methods for retrieving and uploading s3 csv data"

    @staticmethod
    def df_to_bucket(df, file_name, bucket_name):
        "Convert Pandas df to csv and upload to aws bucket."
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_content)

    @staticmethod
    def bucket_to_df(file_name, bucket_name):
        "Get csv from bucket and convert to df"
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read()
        df = pd.read_csv(BytesIO(content))
        return df
