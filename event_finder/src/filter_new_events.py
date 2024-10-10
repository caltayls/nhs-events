import pandas as pd
import os
from dotenv import load_dotenv
from aws_utils.utils import AWSTools

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
ACTIVE_EVENTS = os.getenv("ACTIVE_EVENTS")
# PAST_EVENTS = os.getenv("PAST_EVENTS")

def get_new_events(events_new: pd.Dataframe, events_existing: pd.DataFrame) -> pd.DataFrame:
    """Compares new search to active events dataset.
    returns new events and adds then to active events."""

    # Return a list of urls that are in new df and not in existing.
    urls_existing = set(events_existing.url)
    urls_new = set(events_new.url)

    diff_list = [*urls_new.difference(urls_existing)]
    new_events = events_new.loc[events_new.url.isin(diff_list)]

    #  Check that records don't exist in event history
    # event_history = AWSTools.bucket_to_df('event_history.csv', 'nhs-free-events')
    # new_events = new_events[~new_events[['event_name', 'date', 'location']].isin(event_history.to_dict(orient='list')).all(axis=1)]
    
    return new_events


def update_bucket(events_new, events_existing):
    updated_events = pd.concat([events_existing, events_new], axis=0)
    AWSTools.df_to_bucket(updated_events, ACTIVE_EVENTS, BUCKET_NAME)
