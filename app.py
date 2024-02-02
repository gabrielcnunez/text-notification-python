import sqlite3
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/template', methods=['GET'])
def index():
    conn = get_db_connection()
    templates = conn.execute('SELECT * FROM templates').fetchall()
    conn.close()
    template_list = []
    for template in templates:
        template_list.append({"body": template["body"]})

    return {"templates": template_list}
        