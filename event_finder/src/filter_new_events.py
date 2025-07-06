import pandas as pd

from src.aws_utils import AWSTools


def get_new_events(events_new: pd.DataFrame, events_existing: pd.DataFrame) -> pd.DataFrame:
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


def update_bucket_file(events_new, events_existing, aws_tools: AWSTools, bucket_filename: str):
    updated_events = pd.concat([events_existing, events_new], axis=0)
    aws_tools.df_to_bucket(updated_events, file_name=bucket_filename)
