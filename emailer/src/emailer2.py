from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dataclasses import dataclass, field
from dotenv import load_dotenv
# from pydantic import BaseModel, Field, field_validator

@dataclass
class Client:
    email: str
    app_password: str = field(repr=False)
    emails: list = field(default_factory=list)

    def __str__(self):
        return self.from_

    def __repr__(self):
        return f'<GmailClient {self.from_}>'

    # @classmethod
    # def validate_email_is_gmail(cls, email: str):
    #     if not email.endswith('@gmail.com'):
    #         raise ValueError('Email must be a Gmail address')
    #     return email

    # @classmethod
    # @field_validator('app_password')
    # def validate_app_password(cls, app_password: str):
    #     if not len(app_password) in (16, 19):
    #         feedback = 'App password must be 16 or 19 characters long'
    #         help_link = 'https://support.google.com/accounts/answer/185833?hl=en'
    #         raise ValueError(f'{feedback}. For more information, visit {help_link}')
    #     return app_password

    @classmethod
    def from_env(cls):
        load_dotenv(override=True)
        return cls(
            email = os.getenv('GMAIL_EMAIL'),
            app_password = os.getenv('GMAIL_APP_PASSWORD'),
        )

    @property
    def from_(self) -> str:
        # return f'{self.name} <{self.email}>' if self.name else self.email
        return self.email

    def construct_email(self,  to: str | list[str], subject: str, body: str, from_: str | None = None):
        from_ = from_ or self.from_
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = from_
        message['To'] = to
        html_part = MIMEText(body, 'html')
        message.attach(html_part)
        self.emails.append(message)


    def send_emails(self):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(self.email, self.app_password)
            for email in self.emails:
                server.sendmail(email["From"], email["To"], email.as_string())



# @dataclass
# class Email:
#     from_: str
#     to: str
#     subject: str
#     body: str

#     def __str__(self):
#         return f'From: {self.from_}\nTo: {self.to}\nSubject: {self.subject}\n\n{self.body}'
    
if __name__ == "__main__":
    client = Client.from_env()
    client.construct_email("callumtaylor955@gmail.com", "test html", "<h1>test!</h1>")
    client.send_emails()