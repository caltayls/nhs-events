from src.parse_events import EventParser
from src.utils import update_active_events

def lamba_handler(event, context):
    "aws lambda func handler"
    print("Finding events...")
    current_events_df = EventParser.get_events()
    return {
        'status': '200',
        'data': current_events_df.to_json()
    }
