import sqlite3
import os
from pathlib import Path

def get_connection():
    """Get database connection. Database is stored in project root."""
    project_root = Path(__file__).parent.parent.parent
    db_path = project_root / "documents.db"
    return sqlite3.connect(str(db_path))

def save_document(image_path, ocr_text, clean_text, summary):
    """Save document data to the database."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO documents (image_path, ocr_text, clean_text, summary)
        VALUES (?, ?, ?, ?)
    """, (image_path, ocr_text, clean_text, summary))

    conn.commit()
    conn.close()
