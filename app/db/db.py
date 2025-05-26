'''db/db.py'''
import sqlite3


DB_PATH = "data/database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Prüfe, ob Tabelle schon existiert
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='users_to_embed';
    """)
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute("""
            CREATE TABLE users_to_embed (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supabase_id TEXT UNIQUE,
                name TEXT NOT NULL,
                bio TEXT NOT NULL,
                embedding BLOB,
                updated_at TEXT NOT NULL
            );
        """)
        print("✅ Tabelle users_to_embed neu erstellt.")

    else:
        print("ℹ️ Tabelle users_to_embed bereits vorhanden.")

    conn.commit()
    conn.close()