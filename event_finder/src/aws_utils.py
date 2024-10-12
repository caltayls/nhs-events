from io import BytesIO, StringIO
import boto3
from botocore.exceptions import ClientError
import pandas as pd



class AWSTools:
    "Static methods for retrieving and uploading s3 csv data"
    s3 = boto3.client('s3', region_name='eu-west-2')

    @classmethod
    def df_to_bucket(cls, df, file_name, bucket_name):
        "Convert Pandas df to csv and upload to aws bucket."
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        cls.s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_content)

    @classmethod
    def bucket_to_df(cls, file_name, bucket_name):
        "Get csv from bucket and convert to df"

        try:
            response = cls.s3.get_object(Bucket=bucket_name, Key=file_name)
            content = response['Body'].read()
            df = pd.read_csv(BytesIO(content))
            return df
        except ClientError as e:
            # Check if the error is a 404 error (Not Found)
            if e.response['Error']['Code'] == '404':
                print(f"The file {file_name} does not exist in the bucket {bucket_name}. Returning an empty DataFrame.")
            else:
                print(f"Error occurred: {e}")
            # Return an empty DataFrame
            return pd.DataFrame(columns=["event_name", "location", "date", "url", "website", "website_name", "date_end", "created_at"])
