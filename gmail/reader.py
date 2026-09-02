from .auth import get_gmail_service


def get_unread_emails(max_results=10):

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:

        email = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        headers = email["payload"].get("headers", [])

        sender = ""
        subject = ""

        for header in headers:

            if header["name"].lower() == "from":
                sender = header["value"]

            elif header["name"].lower() == "subject":
                subject = header["value"]

        body = extract_body(email["payload"])

        emails.append({
            "id": message["id"],
            "sender": sender,
            "subject": subject,
            "body": body
        })

    return emails


def extract_body(payload):

    body = payload.get("body", {}).get("data")

    if body:
        return body

    parts = payload.get("parts", [])

    for part in parts:

        if part["mimeType"] == "text/plain":

            data = part["body"].get("data")

            if data:
                return data

    return "No readable body found."