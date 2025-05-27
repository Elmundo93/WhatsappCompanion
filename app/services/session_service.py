# app/services/session_service.py

from app.db.db import get_db_connection
from datetime import datetime

def get_user_state(user_number: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT state FROM whatsapp_sessions WHERE user_number = ?", (user_number,))
    row = cursor.fetchone()
    conn.close()
    return row["state"] if row else "initial"

def set_user_state(user_number: str, state: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO whatsapp_sessions (user_number, state, last_updated)
        VALUES (?, ?, ?)
        ON CONFLICT(user_number) DO UPDATE
        SET state = excluded.state,
            last_updated = excluded.last_updated
    """, (user_number, state, now))
    conn.commit()
    conn.close()

def reset_user_state(user_number: str):
    set_user_state(user_number, "initial")


def has_user_synced(user_number: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT has_synced FROM whatsapp_sessions WHERE user_number = ?", (user_number,))
    row = cursor.fetchone()
    conn.close()
    return bool(row and row["has_synced"])

def set_user_synced(user_number: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO whatsapp_sessions (user_number, state, last_updated, has_synced)
        VALUES (?, 'initial', ?, 1)
        ON CONFLICT(user_number) DO UPDATE
        SET has_synced = 1,
            last_updated = excluded.last_updated
    """, (user_number, now))
    conn.commit()
    conn.close()