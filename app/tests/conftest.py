# tests/conftest.py
import os
import sqlite3
import pytest
from app import create_app
from app.db import db
from dotenv import load_dotenv

TEST_DB_PATH = "data/test_database.db"

@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    load_dotenv(".env.test", override=True)

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    os.makedirs("data", exist_ok=True)
    db.DB_PATH = TEST_DB_PATH
    db.init_db()
    yield
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    # Testtabellen neu anlegen
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE whatsapp_sessions (
            user_number TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            last_updated TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE whatsapp_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_number TEXT NOT NULL,
            direction TEXT CHECK(direction IN ('inbound', 'outbound')) NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    def get_test_connection():
        conn = sqlite3.connect(TEST_DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    monkeypatch.setattr("app.db.db.get_db_connection", get_test_connection)