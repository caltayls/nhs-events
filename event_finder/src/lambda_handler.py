from src.parse_events import EventParser
from src.utils import update_active_events

def lamba_handler(event, context):
    "aws lambda func handler"
    print("Finding events...")
    current_events_df = EventParser.new_events()
    print("Updating s3 csv...")
    update_active_events(current_events_df)
