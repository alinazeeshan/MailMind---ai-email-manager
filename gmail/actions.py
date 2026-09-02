import base64
from email.mime.text import MIMEText

from .auth import get_gmail_service


def create_draft(
    recipient,
    subject,
    body
):

    service = get_gmail_service()

    message = MIMEText(body)

    message["to"] = recipient
    message["subject"] = subject

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    draft = {
        "message": {
            "raw": encoded_message
        }
    }

    result = service.users().drafts().create(
        userId="me",
        body=draft
    ).execute()

    return result