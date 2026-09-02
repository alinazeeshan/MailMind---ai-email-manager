import json

from mistralai.client import Mistral

from config import MISTRAL_API_KEY, MISTRAL_MODEL


client = Mistral(
    api_key=MISTRAL_API_KEY
)


def analyze_email(state):

    prompt = f"""
You are an AI email management assistant.

Analyze this email.

FROM:
{state["sender"]}

SUBJECT:
{state["subject"]}

BODY:
{state["body"]}

Return ONLY valid JSON.

Use this exact structure:

{{
    "category": "work|personal|career|promotion|spam|other",
    "priority": "high|medium|low",
    "summary": "short summary",
    "needs_reply": true
}}

Rules:

- high = urgent or time-sensitive
- medium = useful but not urgent
- low = not important
- needs_reply = true only when a response is reasonably expected
"""

    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    content = content.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    result = json.loads(content)

    return {
        **state,
        "category": result["category"],
        "priority": result["priority"],
        "summary": result["summary"],
        "needs_reply": result["needs_reply"]
    }


def decide_action(state):

    if state["category"] == "spam":
        decision = "ignore"

    elif state["needs_reply"]:
        decision = "draft_reply"

    elif state["priority"] == "high":
        decision = "notify"

    else:
        decision = "archive"

    return {
        **state,
        "decision": decision
    }


def generate_reply(state):

    prompt = f"""
Write a professional email reply.

Original sender:
{state["sender"]}

Subject:
{state["subject"]}

Original email:
{state["body"]}

Write ONLY the reply body.

Do not invent facts.

Keep it polite, concise and professional.
"""

    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    reply = response.choices[0].message.content

    return {
        **state,
        "draft_reply": reply
    }