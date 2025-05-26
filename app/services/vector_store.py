# app/services/vector_store.py

import json
import numpy as np
from app.db.models import get_all_users
from app.utils.utils import get_embedding_model

def get_all_embeddings():
    """
    Gibt eine Liste von dicts mit Namen, Bio und numpy-Embedding zurück.
    """
    users = get_all_users()
    return [
        {
            "name": u["name"],
            "bio": u["bio"],
            "embedding": np.array(json.loads(u["embedding"]))
        }
        for u in users if u.get("embedding")
    ]
def generate_embedding_for_text(text: str):
    model = get_embedding_model()
    vec = model.encode(text)
    return vec / np.linalg.norm(vec)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_top_matches(query: str, top_k=5):
    query_vec = generate_embedding_for_text(query)
    candidates = get_all_embeddings()
    scored = [
        (c["name"], cosine_similarity(query_vec, c["embedding"]))
        for c in candidates
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [f"{name} (Score: {score:.2f})" for name, score in scored[:top_k]]