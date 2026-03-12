import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Add the parent directory of 'app' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.customer import Customer
from app.models.country import Country
from app.models.invoice import Invoice

def seed_db():
    """Populates SAP HANA with initial seed data."""
    db = SessionLocal()
    try:
        print("Seeding database...")
        
        # Check if user already exists
        if not db.query(User).filter(User.USER_ID == "d8b00da2-b84f-41d7-bc6f-b0bde022243a").first():
            db_user = User(
                USER_ID="d8b00da2-b84f-41d7-bc6f-b0bde022243a",
                EMAIL="client@test.com",
                NAME="client",
                CLIENT_NAME="DEMO USER",
                ROLE_TYPE=["USER"],
                STATUS="ACTIVE",
                ALLOWED_COUNTRIES=["AO", "NG", "GR"],
                IS_PARTNER=False,
                AUTO_SUBMIT=True,
                API_KEY="pk_Z3OTnqn3wRYFSiCmsLfOUvskRjLCy49c",
                CREATED_AT=datetime.fromisoformat("2025-12-22T09:27:58.505743"),
                UPDATED_AT=datetime.fromisoformat("2026-02-20T11:59:37.238376"),
            )
            db.add(db_user)
            print("Seeded User: client@test.com")
        
        # Add a couple of sample countries
        countries_data = [
            {"code": "AO", "name": "Angola"},
            {"code": "NG", "name": "Nigeria"},
            {"code": "GR", "name": "Greece"},
            {"code": "PT", "name": "Portugal"},
            {"code": "SA", "name": "Saudi Arabia"},
        ]
        for c in countries_data:
            if not db.query(Country).filter(Country.COUNTRY_CODE == c["code"]).first():
                db_country = Country(COUNTRY_CODE=c["code"], COUNTRY_NAME=c["name"])
                db.add(db_country)
                print(f"Seeded Country: {c['name']}")

        # Add sample invoices
        invoices_data = [
            {
                "DOC_ID": "FT AO/2026/001",
                "SOURCE_REFERENCE": "March-01",
                "CUSTOMER_NAME": "March Customer",
                "GROSS_AMOUNT": 1200.00,
                "STATUS": "accepted",
                "DOC_TYPE": "Standard Invoice",
                "COUNTRY_CODE": "AO",
                "COUNTRY_NAME": "Angola",
                "HAS_ATTACHMENT": True,
                "CREATED_AT": datetime(2026, 3, 12, 10, 0, 0)
            },
            {
                "DOC_ID": "FT NG/2026/005",
                "SOURCE_REFERENCE": "March-05",
                "CUSTOMER_NAME": "Acme NG",
                "GROSS_AMOUNT": 5500.00,
                "STATUS": "pending",
                "DOC_TYPE": "Standard Invoice",
                "COUNTRY_CODE": "NG",
                "COUNTRY_NAME": "Nigeria",
                "HAS_ATTACHMENT": False,
                "CREATED_AT": datetime(2026, 3, 12, 11, 0, 0)
            },
            {
                "DOC_ID": "FT GR/2026/99",
                "SOURCE_REFERENCE": "Old-01",
                "CUSTOMER_NAME": "Ancient Greek",
                "GROSS_AMOUNT": 999.99,
                "STATUS": "rejected",
                "DOC_TYPE": "Debit Note",
                "COUNTRY_CODE": "GR",
                "COUNTRY_NAME": "Greece",
                "HAS_ATTACHMENT": True,
                "CREATED_AT": datetime(2026, 1, 15, 9, 0, 0)
            },
            {
                "DOC_ID": "FT FT3926S2781N/151",
                "SOURCE_REFERENCE": "Test Round",
                "CUSTOMER_NAME": "Test 1234",
                "GROSS_AMOUNT": 6800.00,
                "STATUS": "accepted",
                "DOC_TYPE": "Standard Invoice",
                "COUNTRY_CODE": "AO",
                "COUNTRY_NAME": "Angola",
                "HAS_ATTACHMENT": True
            },
            {
                "DOC_ID": "FT FT3926S2781N/149",
                "SOURCE_REFERENCE": "Test Round",
                "CUSTOMER_NAME": "Test 1234",
                "GROSS_AMOUNT": 115400.00,
                "STATUS": "rejected",
                "DOC_TYPE": "Standard Invoice",
                "COUNTRY_CODE": "AO",
                "COUNTRY_NAME": "Angola",
                "HAS_ATTACHMENT": False
            },
            {
                "DOC_ID": "FT NG8801S1234N/08",
                "SOURCE_REFERENCE": "NG-Invoice-08",
                "CUSTOMER_NAME": "Qualquer XYZ",
                "GROSS_AMOUNT": 45000.00,
                "STATUS": "pending",
                "DOC_TYPE": "Standard Invoice",
                "COUNTRY_CODE": "NG",
                "COUNTRY_NAME": "Nigeria",
                "HAS_ATTACHMENT": True
            }
        ]

        for inv in invoices_data:
            if not db.query(Invoice).filter(Invoice.DOC_ID == inv["DOC_ID"]).first():
                db_invoice = Invoice(**inv)
                db.add(db_invoice)
                print(f"Seeded Invoice: {inv['DOC_ID']}")

        # Add sample customers
        customers_data = [
            {
                "ID": "d0185845-ea6a-40d4-8634-4c664017190a",
                "CUSTOMER_ID": "302291",
                "CUSTOMER_TAX_ID": "5001441337",
                "CUSTOMER_NAME": "Temp",
                "CUSTOMER_COUNTRY_CODE": "AO",
                "CREATED_AT": datetime.fromisoformat("2026-01-22T16:59:38.572009+00:00"),
                "UPDATED_AT": datetime.fromisoformat("2026-03-02T11:27:07.384871+00:00")
            },
            {
                "ID": "f7fd0547-f85d-43aa-beb4-364a4234a4df",
                "CUSTOMER_ID": "CUST-004",
                "CUSTOMER_TAX_ID": "5000471283",
                "CUSTOMER_NAME": "Test 1234",
                "CUSTOMER_ADDRESS_LINE1": "Rua Test",
                "CUSTOMER_ADDRESS_LINE2": "Luanda linha 2",
                "CUSTOMER_STATE": "Luanda state",
                "CUSTOMER_COUNTRY_CODE": "AO",
                "CUSTOMER_POSTAL_CODE": "12345",
                "CREATED_AT": datetime.fromisoformat("2026-01-16T11:07:00.510035+00:00"),
                "UPDATED_AT": datetime.fromisoformat("2026-02-13T15:09:15.859397+00:00")
            },
            {
                "ID": "ad86d6dc-94dc-4ba1-b69f-f0c331241ee2",
                "CUSTOMER_ID": "CUST-003",
                "CUSTOMER_TAX_ID": "123456789",
                "CUSTOMER_NAME": "Qualquer XYZ",
                "CUSTOMER_COUNTRY_CODE": "PT",
                "CREATED_AT": datetime.fromisoformat("2026-01-16T08:25:13.430821+00:00"),
                "UPDATED_AT": datetime.fromisoformat("2026-01-23T12:07:46.498036+00:00")
            }
        ]

        for cust in customers_data:
            if not db.query(Customer).filter(Customer.ID == cust["ID"]).first():
                db_customer = Customer(**cust)
                db.add(db_customer)
                print(f"Seeded Customer: {cust['CUSTOMER_NAME']}")

        db.commit()
        print("Successfully seeded initial data!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
