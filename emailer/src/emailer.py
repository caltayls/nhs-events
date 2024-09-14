import base64
from dotenv import load_dotenv
from email.mime.text import MIMEText
import os.path
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
		"expiry": datetime.strptime(os.getenv('EXPIRY'), '%Y-%m-%dT%H:%M:%S.%fZ'),
		"scopes": os.getenv('SCOPES').split()
	})

	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
			os.environ['TOKEN'] = creds.token
			os.environ['EXPIRY'] = str(creds.expiry)

	return creds


creds = get_creds()
service = build('gmail', 'v1', credentials=creds)
message = MIMEText('This is the body of the email')
message['to'] = 'callumtaylor955@gmail.com'
message['subject'] = 'Email Subject'
create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
try:
	message = (service.users().messages().send(userId="me", body=create_message).execute())
	print(F'sent message to {message} Message Id: {message["id"]}')
except HTTPError as error:
	print(F'An error occurred: {error}')
