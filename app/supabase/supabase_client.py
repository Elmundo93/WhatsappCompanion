'''supabase/supabase_client.py'''
from supabase import create_client
from app.utils.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)