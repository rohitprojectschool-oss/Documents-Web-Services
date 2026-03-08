import os
from sqlalchemy import create_engine, func, case, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sys

# Add parent dir to path to import models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.invoice import Invoice

load_dotenv()

HANA_DB_HOST = os.getenv("HANA_DB_HOST")
HANA_DB_PORT = os.getenv("HANA_DB_PORT")
HANA_DB_USER = os.getenv("HANA_DB_USER")
HANA_DB_PASSWORD = os.getenv("HANA_DB_PASSWORD")

# Use Port 443 with encrypt=true for HANA Cloud
HANA_URL = f"hana://{HANA_DB_USER}:{HANA_DB_PASSWORD}@{HANA_DB_HOST}:{HANA_DB_PORT}?encrypt=true"

engine = create_engine(HANA_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_analytics():
    db = SessionLocal()
    try:
        print("Testing basic connection...")
        db.execute(text("SELECT 1 FROM DUMMY")).fetchone()
        print("Connection successful.")

        print("Testing Country Aggregation...")
        country_agg = db.query(
            Invoice.COUNTRY_CODE,
            Invoice.COUNTRY_NAME,
            func.count(Invoice.DOC_ID).label('total'),
            func.sum(case((Invoice.STATUS == 'accepted', 1), else_=0)).label('accepted')
        ).group_by(Invoice.COUNTRY_CODE, Invoice.COUNTRY_NAME).all()
        print(f"Country Agg success: {len(country_agg)} rows")

        print("Testing Monthly Trends with MONTHNAME...")
        # Note: HANA's function for month name is often MONTHNAME
        month_label = func.monthname(Invoice.CREATED_AT).label('month')
        monthly_agg = db.query(
            month_label,
            Invoice.COUNTRY_CODE,
            func.count(Invoice.DOC_ID).label('count')
        ).group_by(month_label, Invoice.COUNTRY_CODE).all()
        
        for row in monthly_agg:
            print(f"Row: {row.month}, {row.COUNTRY_CODE}, {row.count}")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_analytics()
