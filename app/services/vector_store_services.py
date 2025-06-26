# app/services/vector_store_services.py

import json
import numpy as np
from app.db.models import get_all_users
from app.utils.utils import get_embedding_model

def matches_category_keywords(text: str, query: str) -> bool:
    category_keywords = {
        "garten": ["garten", "gärtnern", "beet", "pflanzen", "rasen", "hecke", "unkraut", "pflanzenpflege"],
        "haushalt": ["haushalt", "putzen", "reinigen", "sauber", "wohnung", "aufräumen", "haushaltshilfe"],
        "handwerk": ["handwerk", "werkzeug", "bauen", "reparieren", "schrauben", "bohren", "montage"],
        "gastro": ["kochen", "backen", "küche", "lebensmittel", "essen", "gastronomie", "kellnern"],
        "gesellschaft": ["besuch", "unterhalten", "gesellschaft", "vorlesen", "sprechen", "plaudern", "spazieren"],
        "bildung": ["nachhilfe", "lernen", "schule", "lesen", "schreiben", "bildung", "hausaufgabenhilfe"],
    }

    text_lower = text.lower()
    query_lower = query.lower()

    for keywords in category_keywords.values():
        if any(k in text_lower for k in keywords) and any(k in query_lower for k in keywords):
            return True
    return False

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

    def boost_score_if_keywords_present(bio: str, query: str, base_score: float) -> float:
        if matches_category_keywords(bio, query):
            return base_score + 0.35  # Boost
        return base_score

    scored = []
    for c in candidates:
        sim = cosine_similarity(query_vec, c["embedding"])
        if sim < min_score:
            continue

        boosted_score = boost_score_if_keywords_present(c["bio"], query, sim)
        scored.append({
            "name": c["name"],
            "bio": c["bio"],
            "score": float(boosted_score)
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]