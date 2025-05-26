import os
from dotenv import load_dotenv

load_dotenv()

# Supabase
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

# Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
TWILIO_TEMPLATE_SID = os.getenv("TWILIO_TEMPLATE_SID")

# System
VECTOR_DB_PATH = os.environ["VECTOR_DB_PATH"]
FLASK_ENV = os.getenv("FLASK_ENV", "development")
DB_PATH = os.getenv("DB_PATH", "data/chat.db")  # fallback

# Optional
PORT = int(os.getenv("PORT", 5000))