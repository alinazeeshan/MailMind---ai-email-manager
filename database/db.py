import sqlite3

from config import DATABASE_NAME


def get_connection():

    return sqlite3.connect(DATABASE_NAME)


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            category TEXT,
            priority TEXT,
            summary TEXT,
            needs_reply INTEGER,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_email(data):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO emails
        (
            id,
            sender,
            subject,
            category,
            priority,
            summary,
            needs_reply
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["sender"],
        data["subject"],
        data["category"],
        data["priority"],
        data["summary"],
        int(data["needs_reply"])
    ))

    connection.commit()
    connection.close()


def get_processed_emails():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM emails
        ORDER BY processed_at DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows