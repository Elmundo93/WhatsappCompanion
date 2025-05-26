from app.supabase.sync import sync_users_from_supabase
from app.db.models import get_all_users

def test_supabase_sync_runs():
    sync_users_from_supabase()
    users = get_all_users()
    assert isinstance(users, list)
    assert any("embedding" in u and u["embedding"] is not None for u in users)