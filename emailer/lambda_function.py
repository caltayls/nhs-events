from src import emailer2, utils

def lambda_handler(event, context):
    
    events_html = event["response"]
    users = utils.get_users()
    print(f"{len(users)} returned.")

    client = emailer2.Client.from_env()
    for user in users:
        client.construct_email(
            to = user['email'],
            subject="New Events",
            body=events_html
        )
    client.send_emails()

    return {
        'status': 200
    }
        