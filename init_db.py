import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO templates (body) VALUES ('Hello, (personal). How are you today, (personal)?')")

cur.execute("INSERT INTO templates (body) VALUES ('Goodbye, (personal). Have a great day, (personal)!')")

cur.execute("INSERT INTO notifications (phone_number, personalization, template_id) VALUES (?, ?, ?)",
            ('+15208675309', 'Jenny', 1))

cur.execute("INSERT INTO notifications (phone_number, personalization, template_id) VALUES (?, ?, ?)",
            ('+12125554444', 'Linda', 2))

cur.execute("INSERT INTO notifications (phone_number, personalization, template_id) VALUES (?, ?, ?)",
            ('+12022051600', 'Joe', 1))

connection.commit()
connection.close()