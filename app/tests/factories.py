import numpy as np
from datetime import datetime
from app.db.models import insert_user

def create_dummy_user(index=1):
    supabase_id = f"test-id-{index}"
    name = f"User {index}"
    bio = f"Hilfsbereiter Mensch #{index}"
    vec = np.random.rand(384).astype(np.float32)
    updated_at = datetime.utcnow().isoformat()

    insert_user(supabase_id, name, bio, vec, updated_at)
    return supabase_id