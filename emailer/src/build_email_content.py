from io import BytesIO
import pandas as pd
import os
import boto3
from dotenv import load_dotenv
from datetime import datetime
from emailer.src import utils, html_generator
from aws_utils.utils import AWSTools

load_dotenv()

AWS_BUCKET = os.getenv("AWS_BUCKET")
SOURCE_EMAIL_ADDRESS = os.getenv("SOURCE_EMAIL_ADDRESS")
ACTIVE_EVENTS_FILENAME = os.getenv("ACTIVE_EVENTS_FILENAME")
LOCATIONS_CSV_FILENAME = os.getenv("LOCATIONS_CSV_ENDPOINT")

s3 = boto3.client('s3')
location_df = AWSTools.bucket_to_df(LOCATIONS_CSV_FILENAME, AWS_BUCKET)
events_df = AWSTools.bucket_to_df(ACTIVE_EVENTS_FILENAME, AWS_BUCKET)

today = datetime.today()

def user_html(user: pd.Series) -> dict[str]:
    freq = user['freq']
    user_locs = utils.get_areas_from_county(user, location_df)
    # locs_str = '|'.join(user_locs.values)

    events_df = events_df[events_df['location'].isin(user_locs)]

    weekly_events = events_df[events_df['created_at'].dt.isocalendar()["week"] == today.isocalendar()[1]] 
    today_events = events_df[events_df['created_at'].dt.date == today.date()]
    hourly_events = today_events[today_events['created_at'].dt.hour == today.hour]

    if freq == "hourly":
        html =  html_generator.render_html(hourly_events)
    elif freq == "daily":
        html = html_generator.render_html(today_events)
    else:
        html = html_generator.render_html(weekly_events)
    
    return {
        "email": user['email'],
        'html': html
    }


