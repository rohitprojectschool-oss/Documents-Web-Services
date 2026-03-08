import sys
import os

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import engine
from app.db.base import Base

def create_tables():
    """
    Creates all tables in SAP HANA based on our models.
    Make sure your .env has the correct HANA_DB_HOST before running.
    """
    print("Creating tables in SAP HANA...")
    try:
        # metadata.create_all() will check for existing tables first
        Base.metadata.create_all(bind=engine)
        print("Successfully created tables: USERS, INVOICES, CUSTOMERS, COUNTRIES")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
