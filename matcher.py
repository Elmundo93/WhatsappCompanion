from vector_store import get_vectorstore
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
vs = get_vectorstore()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_matches(user_input, top_k=3):
    query_vec = model.encode(user_input)
    candidates = vs['data']
    scored = [(user['name'], cosine_similarity(query_vec, user['embedding'])) for user in candidates]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [f"{name} (Score: {score:.2f})" for name, score in scored[:top_k]]