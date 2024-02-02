import json
import pytest
from app import app, get_db_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_template_index_endpoint(client):
    response = client.get('/template')

    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'body' in data[0]

def test_template_show_endpoint_happy(client):
    template_id = 1

    response = client.get(f'/template/{template_id}')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data['id'] == 1
    assert data['body'] == 'Hello, (personal). How are you today, (personal)?'

def test_template_show_endpoint_sad(client):
    non_existing_template_id = 999999
    response = client.get(f'/template/{non_existing_template_id}')

    assert response.status_code == 404
    assert b'Template not found' in response.data

def test_create_template_endpoint_happy(client):
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

def test_create_template_endpoint_sad(client):
    template_data = {
        'body': ''
    }
    response = client.post('/template', json=template_data)

    assert response.status_code == 400
    assert b'Template body cannot be blank' in response.data

def test_update_template_endpoint_happy(client):
    create_response = client.post('/template', json={'body': 'Happy birthday, (personal)!'})
    assert create_response.status_code == 201
    created_template = json.loads(create_response.data)
    template_id = created_template['id']

    updated_body = 'Many happy returns, (personal)!'
    update_response = client.put(f'/template/{template_id}', json={'body': updated_body})
    assert update_response.status_code == 200

    get_response = client.get(f'/template/{template_id}')
    assert get_response.status_code == 200
    retrieved_template = json.loads(get_response.data)
    assert retrieved_template['body'] == updated_body

    with get_db_connection() as conn:
        conn.execute('DELETE FROM templates WHERE id = ?', (retrieved_template['id'],))
        conn.commit()

def test_update_template_sad_path_no_record(client):
    non_existing_template_id = 999999
    response = client.get(f'/template/{non_existing_template_id}')

    assert response.status_code == 404
    assert b'Template not found' in response.data

def test_update_template_sad_path_blank_body(client):
    create_response = client.post('/template', json={'body': 'Happy birthday, (personal)!'})
    assert create_response.status_code == 201
    created_template = json.loads(create_response.data)
    template_id = created_template['id']

    update_response = client.put(f'/template/{template_id}', json={'body': ''})
    
    assert update_response.status_code == 400
    assert b'Template body cannot be blank' in update_response.data

    with get_db_connection() as conn:
        conn.execute('DELETE FROM templates WHERE id = ?', (created_template['id'],))
        conn.commit()

def test_notification_index_endpoint(client):
    response = client.get('/notification')

    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'phone_number' in data[0]
    assert 'personalization' in data[0]
    assert 'template_id' in data[0]