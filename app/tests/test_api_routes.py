import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_search_endpoint(client):
    response = client.get("/search?q=garten")
    assert response.status_code == 200
    assert isinstance(response.json, list)