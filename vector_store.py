import json
from sentence_transformers import SentenceTransformer

def get_vectorstore():
    with open("data/users_embeddings.json", "r") as f:
        return json.load(f)

def generate_vectorstore_from_users(user_list):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    data = []
    for user in user_list:
        embedding = model.encode(user['bio'])
        data.append({
            "name": user['name'],
            "bio": user['bio'],
            "embedding": embedding.tolist()
        })
    with open("data/users_embeddings.json", "w") as f:
        json.dump({"data": data}, f)