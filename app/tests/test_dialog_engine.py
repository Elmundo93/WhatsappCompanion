# tests/test_dialog_engine.py

import pytest
from app.twilio.dialog_engine import get_next_response
from app.services.session_service import set_user_state, get_user_state

@pytest.fixture
def dummy_number():
    return "+49123456789"

def test_empty_history(dummy_number):
    set_user_state(dummy_number, "initial")
    state = get_user_state(dummy_number)
    print("🔍 STATE:", state)
    response = get_next_response(dummy_number, [])
    print("🔁 RESPONSE:", response)
    assert "Hallo" in response

def test_search_help_option(dummy_number):
    set_user_state(dummy_number, "awaiting_help_request")
    history = [{"direction": "inbound", "message": "Ich brauche jemanden für meinen Garten"}]
    response = get_next_response(dummy_number, history)
    assert "niemanden gefunden" in response or "passt" in response

def test_offer_help_option(dummy_number):
    set_user_state(dummy_number, "awaiting_help_offer")
    history = [{"direction": "inbound", "message": "Ich helfe gerne bei Handwerk"}]
    response = get_next_response(dummy_number, history)
    assert "niemanden gefunden" in response or "passt" in response

def test_profile_option(dummy_number):
    set_user_state(dummy_number, "initial")
    history = [{"direction": "inbound", "message": "3"}]
    response = get_next_response(dummy_number, history)
    assert "Profil" in response

def test_invalid_option(dummy_number):
    set_user_state(dummy_number, "initial")
    history = [{"direction": "inbound", "message": "42"}]
    response = get_next_response(dummy_number, history)
    assert "nicht verstanden" in response