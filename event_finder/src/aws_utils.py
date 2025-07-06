from io import BytesIO, StringIO
import boto3
from botocore.exceptions import ClientError
import pandas as pd



class AWSTools:
    "Static methods for retrieving and uploading s3 csv data"

    def __init__(self, region_name: str, bucket_name: str):
        self.s3 = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name

    def df_to_bucket(self, df: pd.DataFrame, file_name: str):
        "Convert df to csv and upload to aws bucket."
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        self.s3.put_object(Bucket=self.bucket_name, Key=file_name, Body=csv_content)

    def bucket_to_df(self, file_name):
        "Get csv from bucket and convert to df"

        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=file_name)
            content = response['Body'].read()
            df = pd.read_csv(BytesIO(content))
            return df
        except ClientError as e:
            # Check if the error is a 404 error (Not Found)
            if e.response['Error']['Code'] == '404':
                print(f"The file {file_name} does not exist in the bucket {self.bucket_name}. Returning an empty DataFrame.")
            else:
                print(f"Error occurred: {e}")
            # Return an empty DataFrame
            return pd.DataFrame(columns=["event_name", "location", "date", "url", "website", "website_name", "date_end", "created_at"])
