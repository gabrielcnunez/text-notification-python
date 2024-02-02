import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_index_endpoint(client):
    response = client.get('/template')

    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'body' in data[0]
