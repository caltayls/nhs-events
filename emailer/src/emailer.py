import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from email.mime.text import MIMEText
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from requests import HTTPError
from datetime import datetime


load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_creds():
    """Shows basic usage of the Gmail API."""

    creds = Credentials(**{
        "token": os.getenv('TOKEN'),
        "refresh_token": os.getenv('REFRESH_TOKEN'),
        "token_uri": os.getenv('TOKEN_URI'),
        "client_id": os.getenv('CLIENT_ID'),
        "client_secret": os.getenv('CLIENT_SECRET'),
        "expiry": datetime.strptime(
            os.getenv('EXPIRY'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ),
        "scopes": os.getenv('SCOPES').split()
    })

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            os.environ['TOKEN'] = creds.token
            os.environ['EXPIRY'] = str(creds.expiry)

    return creds


def send_email_sync(email_address, body_html):
    creds = get_creds()
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(body_html, 'html')
    message['to'] = email_address
    message['subject'] = 'Email Subject'
    create_message = {
        'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
    }
    try:
        message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(f'An error occurred: {error}')
        print(f'Could not sent email to {email_address}')


async def send_email_async(executor, email_address, body_html):
    loop = asyncio.get_event_loop()

    await loop.run_in_executor(
        executor,
        send_email_sync,
        email_address,
        body_html
    )


async def email_all_subscribers(email_addr_html_content: list[dict]) -> None:
    tasks = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for email in email_addr_html_content:
            email_address = email['email_address']
            body_html = email['html']
            task = send_email_async(executor, email_address, body_html)
            tasks.append(task)
        await asyncio.gather(*tasks)


def lambda_handler(event, context):
    email_and_content = event['sdfsdf']['sdfsdfsdf']
    asyncio.run(email_all_subscribers(email_and_content))



if __name__ == '__main__':
    # send_email('callumtaylor955@gmail.com', "<p>tooooo</p>")
    email_and_content = [
        {
            'email_address': 'callumtaylor955@gmail.com',
            'html': '<p> qwyer </p>'
        },

        {
            'email_address': 'callumtaylor955@gmail.com',
            'html': '<p> sdgfadfg </p>'
        },

        {
            'email_address': 'callumtaylor955@gmail.com',
            'html': '<p> sdfghsdfggfdgfadfg </p>'
        },
    ]

    asyncio.run(email_all_subscribers(email_and_content))
    
