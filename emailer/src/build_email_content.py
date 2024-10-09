from io import BytesIO
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime
from emailer.src import utils, html_generator
from aws_utils.utils import AWSTools


def init():
    load_dotenv()

    AWS_BUCKET = os.getenv("AWS_BUCKET")
    SOURCE_EMAIL_ADDRESS = os.getenv("SOURCE_EMAIL_ADDRESS")
    ACTIVE_EVENTS_FILENAME = os.getenv("ACTIVE_EVENTS_FILENAME")
    LOCATIONS_CSV_FILENAME = os.getenv("LOCATIONS_CSV_ENDPOINT")

    location_df = AWSTools.bucket_to_df(LOCATIONS_CSV_FILENAME, AWS_BUCKET)
    events_df = AWSTools.bucket_to_df(ACTIVE_EVENTS_FILENAME, AWS_BUCKET)


def user_html(user: dict, events_df: pd.DataFrame) -> dict[str]:
    
    # Some locs are just venue so make it difficult to locate. so will ignore location filter
    # events_df = get_events_based_on_loc(user, location_df, events_df)
    
    events_df = get_events_based_on_freq(user, events_df)
    html = html_generator.render_html(events_df)
    
    return {
        "email": user['email'],
        'html': html
    }


def get_events_based_on_freq(user: pd.Series, events: pd.DataFrame) -> pd.DataFrame:
    
    freq = user['freq']
    today = datetime.today()
    today_events = events[events['created_at'].dt.date == today.date()]
    hourly_events = today_events[today_events['created_at'].dt.hour == today.hour]

    if freq == 'weekly':
        return events[events['created_at'].dt.isocalendar()["week"] == today.isocalendar()[1]]
    elif freq == 'daily':
        return today_events
    elif freq == 'hourly':
        return hourly_events



def get_events_based_on_loc(user: pd.Series, locations: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    # Some locs are just venue so make it difficult to locate. so will ignore location filter

    user_locs = utils.get_areas_from_county(user, locations)
    user_locs = user_locs.str.replace('-' , ' ')
    user_locs = user_locs.str.replace('&' , 'and')
    locs_str = '|'.join(user_locs.values)

    events['location'] = events['location'].str.replace('-' , ' ')
    events['location'] = events['location'].str.replace('&' , 'and')

    events = events[events['location'].str.contains(locs_str, case=False, regex=True)]
