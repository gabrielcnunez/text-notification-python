import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/template', methods=['GET'])
def index():
    conn = get_db_connection()
    query = 'SELECT id, body FROM templates'
    templates = conn.execute(query).fetchall()
    conn.close()

    template_list = [{'id': template['id'], 'body': template['body']} for template in templates]

    return jsonify(template_list)

@app.route('/template/<int:id>', methods=['GET'])
def show(id):
    conn = get_db_connection()
    query = 'SELECT * FROM templates WHERE id = ?'
    template = conn.execute(query, (id,)).fetchone()
    conn.close()
    if template is None:
        return 'Template not found', 404
    
    return jsonify(dict(template))

@app.route('/template', methods=['POST'])
def create_template():
    template_data = request.json
    
    if 'body' not in template_data or not template_data['body'].strip():
        return 'Template body cannot be blank', 400
    
    conn = get_db_connection()
    query = 'INSERT INTO templates (body) VALUES (?)'
    cursor = conn.execute(query, (template_data['body'],))
    template_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({'id': template_id, 'body': template_data['body']}), 201

@app.route('/template/<int:id>', methods=['PUT'])
def update_template_put(id):
    conn = get_db_connection()

    existing_template = conn.execute('SELECT * FROM templates WHERE id = ?', (id,)).fetchone()
    if existing_template is None:
        conn.close()
        return 'Template not found', 404

    updated_template_data = request.json

    if 'body' not in updated_template_data or not updated_template_data['body'].strip():
        conn.close()
        return 'Template body cannot be blank', 400

    query = 'UPDATE templates SET body = ? WHERE id = ?'
    conn.execute(query, (updated_template_data['body'], id))
    
    conn.commit()
    conn.close()

    return jsonify({'id': id, 'body': updated_template_data['body']}), 200

@app.route('/notification', methods=['GET'])
def get_all_notifications():
    conn = get_db_connection()
    query = 'SELECT * FROM notifications'
    notes = conn.execute(query).fetchall()
    conn.close()

    notes_list = [{'id': note['id'], 'phone_number': note['phone_number'], 'personalization': note['personalization'], 'template_id': note['template_id']} for note in notes]

    return jsonify(notes_list)