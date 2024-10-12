import pandas as pd
from src import emailer2, build_email_content, utils

def lambda_handler(event, context):
    
    events = event["events"]
    event_df = pd.DataFrame(events)
    users = utils.get_users()
    print(f"{len(users)} returned.")



    messages = [build_email_content.user_html(user, event_df) for user in users]

    client = emailer2.Client.from_env()
    for message in messages:
        client.construct_email(
            to = message['email'],
            subject="New Events",
            body=message['html']
        )
    client.send_emails()

    return {
        'status': 200
    }
        