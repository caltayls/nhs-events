
import datetime
import pandas as pd
from aws_utils.utils import AWSTools

def lambda_handler(event, context):
    """To be run at 0000 every day.
    removes expired events from active dataset and stores them in past events dataset"""
    active_events_df = AWSTools.bucket_to_df('active_events.csv', 'nhs-free-events')
    active_events_df.date_end = pd.to_datetime(active_events_df.date_end)
    today = datetime.datetime.now().date()
    expired_events = active_events_df.query("date_end < @today")
    active_events = active_events_df.query("date_end >= @today")

    AWSTools.df_to_bucket(active_events, 'active_events.csv', 'nhs-free-events')

    # update past events
    event_history_df = AWSTools.bucket_to_df('event_history.csv', 'nhs-free-events')
    event_history_df = pd.concat((event_history_df, expired_events), axis=0)
    event_history_df = event_history_df.drop(['url', 'website'], axis=1)
    AWSTools.df_to_bucket(event_history_df, 'event_history.csv', 'nhs-free-events')