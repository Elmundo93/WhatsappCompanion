import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_invalid_request(client):
    res = client.post("/webhook/twilio", data={})
    assert res.status_code == 400
    assert b"Invalid request" in res.data

def test_valid_request(monkeypatch, client):
    # Mocking Hilfsfunktionen
    monkeypatch.setattr("app.utils.utils.is_valid_whatsapp_request", lambda req: True)
    monkeypatch.setattr("app.db.chat_history.save_message", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.db.chat_history.get_history", lambda num, limit=10: [{"direction": "inbound", "message": "1"}])
    monkeypatch.setattr("app.utils.twilio_client.send_whatsapp_reply", lambda to, msg: None)

    res = client.post("/webhook/twilio", data={"From": "whatsapp:+491234567890", "Body": "1"})
    assert res.status_code == 200
    assert b"OK" in res.data