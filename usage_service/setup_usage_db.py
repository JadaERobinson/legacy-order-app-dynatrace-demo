import sqlite3

conn = sqlite3.connect('usage.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE usage (
    customer_id TEXT,
    data_usage INTEGER
)
''')

cursor.executemany('INSERT INTO usage VALUES (?, ?)', [
    ("1", 2000),
    ("2", 5000),
    ("3", 300)
])

conn.commit()
conn.close()
