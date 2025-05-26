'''supabase/sync.py'''
from app.supabase.supabase_client import supabase
from app.db.models import insert_user
from app.vector_store import add_vector, delete_vector  # NEU
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def sync_users_from_supabase():
    response = supabase.table("Users").select("id, vorname, bio, created_at").execute()
    for user in response.data:
        vec = model.encode(user["bio"])
        vec = vec / np.linalg.norm(vec)  # normalize

        # 1. SQLite speichern oder aktualisieren
        insert_user(
            supabase_id=user["id"],
            name=user["vorname"],
            bio=user["bio"],
            embedding_vector=vec,
            updated_at=user["created_at"]
        )

        # 2. VectorStore aufräumen (falls Duplikate)
        delete_vector(user["id"])  # ← sicherstellen, dass alt gelöscht ist

        # 3. Vector hinzufügen
        add_vector(
            id=user["id"],
            vector=vec.tolist(),
            metadata={
                "name": user["vorname"],
                "bio": user["bio"]
            }
        )

    print("✅ Supabase Sync erfolgreich & Vektoren aktualisiert")