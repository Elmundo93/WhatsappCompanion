from app.db.db import get_db_connection
from datetime import datetime

### Nachrichten-Verlauf speichern

def init_whatsapp_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verlaufstabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_number TEXT NOT NULL,
            direction TEXT CHECK(direction IN ('inbound', 'outbound')) NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Session-Tabelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_sessions (
            user_number TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            last_updated TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_message(user_number: str, direction: str, message: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO whatsapp_messages (user_number, direction, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_number, direction, message, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


def get_history(user_number: str, limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT direction, message, timestamp FROM whatsapp_messages
        WHERE user_number = ? ORDER BY timestamp DESC LIMIT ?
    """, (user_number, limit))
    rows = cursor.fetchall()
    conn.close()
    return list(reversed([dict(r) for r in rows]))