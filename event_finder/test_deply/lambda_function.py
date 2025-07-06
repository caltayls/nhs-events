import os
# from pathlib import Path

from dotenv import load_dotenv
from src.parse_events import EventParser
from src.filter_new_events import get_new_events, update_bucket_file
from src.aws_utils import AWSTools
from src.html_generator import render_html

load_dotenv()  # dotenv_path=env_path)
BUCKET_NAME = os.getenv("AWS_BUCKET")
ACTIVE_EVENTS_FILENAME = os.getenv("ACTIVE_EVENTS_FILENAME")
REGION = os.getenv("BUCKET_REGION")

def lambda_handler(event, context):
    print("Finding events...")
    events = EventParser.get_events()
    print(events)
    aws_tools = AWSTools(region_name=REGION, bucket_name=BUCKET_NAME)
    events_existing = aws_tools.bucket_to_df(ACTIVE_EVENTS_FILENAME)
    events_new = get_new_events(events, events_existing)
    print('new events')
    print(events_new)
    print("updating bucket...")
    update_bucket_file(events_new, events_existing, aws_tools, ACTIVE_EVENTS_FILENAME)
    BODY_HTML = render_html(events_new)
    
    return {'response': BODY_HTML, 'status': 200}



