import os
from dotenv import load_dotenv
from src.parse_events import EventParser
from src.filter_new_events import get_new_events, update_bucket
from aws_utils.utils import AWSTools

load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
ACTIVE_EVENTS = os.getenv("ACTIVE_EVENTS")

def lamba_handler(event, context):
    print("Finding events...")
    events = EventParser.get_events()
    events_existing = AWSTools.bucket_to_df(ACTIVE_EVENTS, BUCKET_NAME)
    events_new = get_new_events(events, events_existing)
    print("updating bucket...")
    update_bucket(events_new, events_existing)

    return {'status': 200}
