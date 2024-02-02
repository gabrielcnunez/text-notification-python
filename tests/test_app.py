import json
import pytest
from app import app, get_db_connection

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

def test_create_endpoint_happy(client):
    template_data = {
        'body': 'Happy birthday, (personal)!'
    }

    response = client.post('/template', json=template_data)
    assert response.status_code == 201
    response_data = json.loads(response.data)

    # Ensure the expected keys are present in the response data
    assert 'id' in response_data
    assert 'body' in response_data
    assert response_data['body'] == template_data['body']

    with get_db_connection() as conn:
        conn.execute('DELETE FROM templates WHERE id = ?', (response_data['id'],))
        conn.commit()

def test_create_endpoint_sad(client):
    template_data = {
        'body': ''
    }
    response = client.post('/template', json=template_data)

    assert response.status_code == 400
    assert b'Template body cannot be blank' in response.data

