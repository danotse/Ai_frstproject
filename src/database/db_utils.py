import sqlite3

def save_ocr(image_path, ocr_text, clean_text):
    conn = sqlite3.connect("documents.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO documents (image_path, ocr_text, clean_text)
        VALUES (?, ?, ?)
    """, (image_path, ocr_text, clean_text))

    conn.commit()
    conn.close()
