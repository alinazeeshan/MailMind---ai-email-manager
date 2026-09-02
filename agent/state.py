from typing import TypedDict


class EmailState(TypedDict, total=False):

    email_id: str
    sender: str
    subject: str
    body: str

    category: str
    priority: str
    summary: str
    needs_reply: bool

    draft_reply: str

    decision: str