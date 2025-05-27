# app/services/vector_store_services.py

import json
import numpy as np
from app.db.models import get_all_users
from app.utils.utils import get_embedding_model

def get_all_embeddings():
    users = get_all_users()
    return [
        {
            "name": u["name"],
            "bio": u["bio"],
            "embedding": u["embedding"]
        }
        for u in users
        if u.get("embedding") is not None
    ]

def generate_embedding_for_text(text: str):
    model = get_embedding_model()
    vec = model.encode(text)
    return vec / np.linalg.norm(vec)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_top_matches(query: str, top_k=5, min_score=0.5):
    query_vec = generate_embedding_for_text(query)
    candidates = get_all_embeddings()
    scored = [
        {
            "name": c["name"],
            "bio": c["bio"],
            "score": cosine_similarity(query_vec, c["embedding"])
        }
        for c in candidates
    ]
    filtered = [c for c in scored if c["score"] >= min_score]
    filtered.sort(key=lambda x: x["score"], reverse=True)
    return filtered[:top_k]