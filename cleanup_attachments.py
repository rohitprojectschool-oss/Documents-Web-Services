import sys
import os
from sqlalchemy import text

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine

def cleanup_orphaned_attachments():
    """Sets HAS_ATTACHMENT to False for records with null FILE_CONTENT."""
    print("Syncing attachment status with database content...")
    with engine.connect() as conn:
        try:
            # Update records where HAS_ATTACHMENT is true but content is missing
            result = conn.execute(text("UPDATE \"INVOICES\" SET \"HAS_ATTACHMENT\" = FALSE WHERE \"FILE_CONTENT\" IS NULL"))
            conn.commit()
            print(f"Updated {result.rowcount} records to remove broken attachment links.")
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_orphaned_attachments()
