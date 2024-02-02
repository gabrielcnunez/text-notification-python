import sqlite3
from flask import Flask, jsonify

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
        