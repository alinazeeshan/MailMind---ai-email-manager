import streamlit as st

from agent.graph import build_graph
from gmail.reader import get_unread_emails
from gmail.actions import create_draft
from database.db import (
    create_tables,
    save_email,
    get_processed_emails
)


st.set_page_config(
    page_title="MailMind",
    page_icon="📧",
    layout="wide"
)


create_tables()

graph = build_graph()


st.title("📧 MailMind")

st.caption(
    "Agentic AI Email Management System"
)


# Sidebar

st.sidebar.header("MailMind")

if st.sidebar.button("🔄 Fetch Unread Emails"):

    try:

        emails = get_unread_emails()

        st.session_state["emails"] = emails

        st.sidebar.success(
            f"{len(emails)} emails loaded."
        )

    except Exception as e:

        st.sidebar.error(str(e))


emails = st.session_state.get(
    "emails",
    []
)


if not emails:

    st.info(
        "Click 'Fetch Unread Emails' to load your Gmail inbox."
    )

else:

    st.subheader(
        f"📬 {len(emails)} Unread Emails"
    )

    for email in emails:

        with st.expander(
            f"📧 {email['subject']}"
        ):

            st.write(
                f"**From:** {email['sender']}"
            )

            st.write(
                f"**Subject:** {email['subject']}"
            )

            st.write(
                email["body"]
            )

            if st.button(
                "🧠 Analyze",
                key=f"analyze_{email['id']}"
            ):

                with st.spinner(
                    "MailMind is analyzing..."
                ):

                    result = graph.invoke({
                        "email_id": email["id"],
                        "sender": email["sender"],
                        "subject": email["subject"],
                        "body": email["body"]
                    })

                save_email(result)

                st.session_state[
                    f"result_{email['id']}"
                ] = result


            result = st.session_state.get(
                f"result_{email['id']}"
            )


            if result:

                st.divider()

                st.subheader("🤖 AI Analysis")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Category",
                        result["category"]
                    )

                with col2:

                    st.metric(
                        "Priority",
                        result["priority"]
                    )

                with col3:

                    st.metric(
                        "Needs Reply",
                        "Yes"
                        if result["needs_reply"]
                        else "No"
                    )

                st.info(
                    f"📝 {result['summary']}"
                )


                if result["decision"] == "draft_reply":

                    st.subheader(
                        "✍️ Suggested Reply"
                    )

                    reply = st.text_area(
                        "Edit before creating draft",
                        value=result["draft_reply"],
                        height=200,
                        key=f"reply_{email['id']}"
                    )

                    if st.button(
                        "📨 Create Gmail Draft",
                        key=f"draft_{email['id']}"
                    ):

                        try:

                            create_draft(
                                recipient=email["sender"],
                                subject="Re: " + email["subject"],
                                body=reply
                            )

                            st.success(
                                "Draft created in Gmail. "
                                "Review it before sending."
                            )

                        except Exception as e:

                            st.error(str(e))


# History

st.divider()

st.subheader("🗂️ Processing History")

history = get_processed_emails()

if history:

    for row in history:

        (
            email_id,
            sender,
            subject,
            category,
            priority,
            summary,
            needs_reply,
            processed_at
        ) = row

        with st.expander(subject):

            st.write(f"**From:** {sender}")
            st.write(f"**Category:** {category}")
            st.write(f"**Priority:** {priority}")
            st.write(f"**Summary:** {summary}")

else:

    st.write(
        "No processed emails yet."
    )