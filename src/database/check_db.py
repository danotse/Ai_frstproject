import sqlite3

conn = sqlite3.connect("documents.db")
cur = conn.cursor()

rows = cur.execute("SELECT id, image_path FROM documents").fetchall()
for row in rows:
    print(row)

conn.close()
