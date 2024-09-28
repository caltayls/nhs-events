import datetime
from io import BytesIO, StringIO
import boto3
import pandas as pd

s3 = boto3.client('s3', region_name='eu-west-2')
ses = boto3.client('ses', region_name='eu-west-2')

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



def events_to_email(new_df, active_events, aws_tools_instance):
    """Compares new search to active events dataset.
    returns new events and adds then to active events."""

    # Return a list of urls that are in newer df and not the other.
    urls_active = set(active_events.url)
    urls_new = set(new_df.url)

    diff_list = [*urls_new.difference(urls_active)]
    new_events_df = new_df.loc[new_df.url.isin(diff_list)]
    today = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M")
    new_events_df['time_added'] = today

    #  Check that records don't exist in event history
    event_history_df = aws_tools_instance.bucket_to_df('event_history.csv', 'nhs-free-events')
    new_events_df = new_events_df[~new_events_df[['event_name', 'date', 'location']].isin(event_history_df.to_dict(orient='list')).all(axis=1)]
    
    return new_events_df