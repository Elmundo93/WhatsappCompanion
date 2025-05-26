# tests/test_session_service.py

import os
import sqlite3
import pytest
from app.services import session_service

# Pfad zur temporären Datenbank für die Tests
TEST_DB_PATH = "data/test_session.db"

@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    # Erstelle neue leere Datenbank
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Erstelle Testtabelle
    cursor.execute("""
        CREATE TABLE whatsapp_sessions (
            user_number TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            last_updated TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    # Monkeypatch für get_db_connection()
    def get_test_connection():
        conn = sqlite3.connect(TEST_DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    monkeypatch.setattr("app.services.session_service.get_db_connection", get_test_connection)
    yield

    # Clean up nach Test
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_get_initial_state():
    state = session_service.get_user_state("+491234")
    assert state == "initial"


def test_set_and_get_state():
    session_service.set_user_state("+491234", "awaiting_help_description")
    state = session_service.get_user_state("+491234")
    assert state == "awaiting_help_description"


def test_reset_state():
    session_service.set_user_state("+491234", "awaiting_help_description")
    session_service.reset_user_state("+491234")
    state = session_service.get_user_state("+491234")
    assert state == "initial"