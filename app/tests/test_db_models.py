from app.db.models import insert_user, get_user, delete_user
import numpy as np
from datetime import datetime

def test_insert_and_get_user():
    supabase_id = "test-id"
    name = "Testuser"
    bio = "Ich helfe gerne im Garten."
    embedding = np.random.rand(384).astype(np.float32)
    updated_at = datetime.utcnow().isoformat()

    insert_user(supabase_id, name, bio, embedding, updated_at)
    user = get_user(1)  # Annahme: ID = 1 (ansonsten ID zurückgeben lassen)

    assert user["name"] == name
    assert isinstance(user["embedding"], np.ndarray)
    delete_user(1)