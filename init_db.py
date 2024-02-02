import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO templates (body) VALUES ('Hello, (personal). How are you today, (personal)?')")

cur.execute("INSERT INTO templates (body) VALUES ('Goodbye, (personal). Have a great day, (personal)!')")

connection.commit()
connection.close()