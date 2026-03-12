import sys
import os
from sqlalchemy import text

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine

def add_column():
    """Adds missing columns to existing tables."""
    print("Adding binary storage columns to PostgreSQL...")
    with engine.connect() as conn:
        try:
            # Check and add FILE_CONTENT
            check_sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='INVOICES' AND column_name='FILE_CONTENT'")
            if not conn.execute(check_sql).fetchone():
                print("Adding FILE_CONTENT to INVOICES table...")
                conn.execute(text("ALTER TABLE \"INVOICES\" ADD COLUMN \"FILE_CONTENT\" BYTEA"))
            
            # Check and add FILE_NAME
            check_sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='INVOICES' AND column_name='FILE_NAME'")
            if not conn.execute(check_sql).fetchone():
                print("Adding FILE_NAME to INVOICES table...")
                conn.execute(text("ALTER TABLE \"INVOICES\" ADD COLUMN \"FILE_NAME\" VARCHAR(255)"))

            # Check and add FILE_MIME_TYPE
            check_sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='INVOICES' AND column_name='FILE_MIME_TYPE'")
            if not conn.execute(check_sql).fetchone():
                print("Adding FILE_MIME_TYPE to INVOICES table...")
                conn.execute(text("ALTER TABLE \"INVOICES\" ADD COLUMN \"FILE_MIME_TYPE\" VARCHAR(100)"))

            conn.commit()
            print("Database columns updated successfully!")
        except Exception as e:
            print(f"Error adding columns: {e}")

if __name__ == "__main__":
    add_column()
