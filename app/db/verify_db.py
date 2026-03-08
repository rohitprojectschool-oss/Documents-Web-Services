import sys
import os
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.country import Country

def verify():
    db = SessionLocal()
    try:
        print("\n--- DATABASE VERIFICATION ---")
        
        # Check Users
        user_count = db.query(User).count()
        print(f"Users found: {user_count}")
        if user_count > 0:
            user = db.query(User).first()
            print(f"  - First User: {user.EMAIL} ({user.NAME})")

        # Check Countries
        country_count = db.query(Country).count()
        print(f"Countries found: {country_count}")
        if country_count > 0:
            countries = db.query(Country).limit(3).all()
            print(f"  - Sample Countries: {', '.join([c.COUNTRY_NAME for c in countries])}")

        print("-----------------------------\n")
    except Exception as e:
        print(f"Connection Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify()
