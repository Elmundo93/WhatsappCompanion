# app/vector_store.py
from app.vector.local_store import LocalVectorStore
from app.vector.remote_store import RemoteVectorStore
import os
from app.db.models import get_all_users

USE_REMOTE = os.getenv("USE_REMOTE", "false").lower() == "true"

store = RemoteVectorStore() if USE_REMOTE else LocalVectorStore()

def add_vector(id: str, vector: list, metadata: dict):
    return store.add_vector(id, vector, metadata)

def query_vector(vector: list, top_k=5):
    return store.query_vector(vector, top_k)

def delete_vector(id: str):
    return store.delete_vector(id)

def rebuild_index():
    reset_store()
    users = get_all_users()
    for user in users:
        if user.get("embedding") is not None:
            metadata = {"name": user["name"], "bio": user["bio"]}
            add_vector(user["supabase_id"], user["embedding"].tolist(), metadata)

def reset_store():
    return store.reset()