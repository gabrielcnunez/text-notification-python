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

def test_show_endpoint_happy(client):
    template_id = 1

    response = client.get(f'/template/{template_id}')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data['id'] == 1
    assert data['body'] == 'Hello, (personal). How are you today, (personal)?'

def test_show_endpoint_sad(client):
    non_existing_template_id = 999999
    response = client.get(f'/template/{non_existing_template_id}')

    assert response.status_code == 404
    assert b'Template not found' in response.data