import asyncio
import pandas as pd
from emailer.src import emailer, build_email_content, utils

def lambda_handler(event, context):
    
    events = event["events"]
    event_df = pd.DataFrame(events)
    users = utils.get_users()

    user_html = [build_email_content.user_html(user, event_df) for user in users]

    asyncio.run(emailer.email_all_subscribers(user_html))

