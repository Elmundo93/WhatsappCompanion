'''db/models.py'''
from app.db.db import get_db_connection
import numpy as np
from datetime import datetime

def insert_user(supabase_id, name, bio, embedding_vector, updated_at):
    conn = get_db_connection()
    cursor = conn.cursor()

    # vector must be np.ndarray (normalized + dtype float32)
    embedding_blob = embedding_vector.astype(np.float32).tobytes()

    cursor.execute("""
        INSERT OR REPLACE INTO users_to_embed
        (supabase_id, name, bio, embedding, updated_at)
        VALUES (?, ?, ?, ?, ?);
    """, (supabase_id, name, bio, embedding_blob, updated_at))

    conn.commit()
    conn.close()


def update_user(user_id, name, bio):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        UPDATE users_to_embed SET name = ?, bio = ?, updated_at = ? WHERE id = ?;
    """, (name, bio, now, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users_to_embed WHERE id = ?;", (user_id,))
    conn.commit()
    conn.close()


def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users_to_embed WHERE id = ?;", (user_id,)).fetchone()
    conn.close()

    if not user:
        return None

    user_dict = dict(user)
    if user_dict["embedding"]:
        user_dict["embedding"] = np.frombuffer(user_dict["embedding"], dtype=np.float32)
    return user_dict

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM users_to_embed;").fetchall()
    conn.close()

    result = []
    for u in users:
        u_dict = dict(u)
        if u_dict["embedding"]:
            u_dict["embedding"] = np.frombuffer(u_dict["embedding"], dtype=np.float32)
        result.append(u_dict)
    return result