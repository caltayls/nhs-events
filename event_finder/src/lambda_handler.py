import os
# from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from src.parse_events import EventParser
from src.filter_new_events import get_new_events, update_bucket
from src.aws_utils import AWSTools
from src.html_generator import render_html

# env_path = Path(__file__).resolve().parent / '.env'
load_dotenv()  # dotenv_path=env_path)
BUCKET_NAME = os.getenv("AWS_BUCKET")
ACTIVE_EVENTS = os.getenv("ACTIVE_EVENTS_FILENAME")

def lambda_handler(event, context):
    print("Finding events...")
    events = EventParser.get_events()
    print('new evs')
    print(events)
    events_existing = AWSTools.bucket_to_df(ACTIVE_EVENTS, BUCKET_NAME)
    events_new = get_new_events(events, events_existing)
    print("updating bucket...")
    update_bucket(events_new, events_existing)
    SENDER = 'callumtaylor955@gmail.com'  # Must be a verified sender in SES
    RECIPIENT = 'callumtaylor955@gmail.com'      
    SUBJECT = f'New Events: {len(events_new)}'

    BODY_HTML = render_html(events_new)

    CHARSET = 'UTF-8'
    ses_client = boto3.client('ses', region_name='eu-west-2')
    # Try to send the email
    try:
        response = ses_client.send_email(
            Source=SENDER,
            Destination={
                'ToAddresses': [
                    RECIPIENT
                ]
            },
            Message={
                'Subject': {
                    'Data': SUBJECT,
                    'Charset': CHARSET
                },
                'Body': {
                    'Html': {
                        'Data': BODY_HTML,
                        'Charset': CHARSET
                    }
                }
            }
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")

    return {'status': 200}

