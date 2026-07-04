import sqlite3

conn = sqlite3.connect("dictionary.db")

cursor = conn.cursor()

cursor.execute("SELECT word, ipa FROM entries")

for row in cursor.fetchall():
    print(row)