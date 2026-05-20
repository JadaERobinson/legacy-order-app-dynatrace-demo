import sqlite3

conn = sqlite3.connect('billing.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE billing (
    customer_id TEXT,
    balance INTEGER
)
''')

cursor.executemany('INSERT INTO billing VALUES (?, ?)', [
    ("1", 100),
    ("2", 250),
    ("3", 75)
])

conn.commit()
conn.close()
