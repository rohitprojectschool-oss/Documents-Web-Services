from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomersResponse, Customer as CustomerSchema
from typing import List

router = APIRouter()

@router.get("", response_model=CustomersResponse)
async def get_customers(db: Session = Depends(get_db)):
    """Fetch all customers from SAP HANA."""
    try:
        # Fetch customers from the database
        db_customers = db.query(Customer).all()
        
        # If no customers in DB, you might want to return empty or mock
        # For this transition, we convert DB models to Pydantic schemas
        customers = []
        for c in db_customers:
            customers.append(CustomerSchema(
                id=c.ID,
                customer_id=c.CUSTOMER_ID,
                customer_tax_id=c.CUSTOMER_TAX_ID,
                customer_name=c.CUSTOMER_NAME,
                customer_email=c.CUSTOMER_EMAIL,
                customer_phone=c.CUSTOMER_PHONE,
                customer_address_line1=c.CUSTOMER_ADDRESS_LINE1,
                customer_address_line2=c.CUSTOMER_ADDRESS_LINE2,
                customer_state=c.CUSTOMER_STATE,
                customer_country_code=c.CUSTOMER_COUNTRY_CODE,
                customer_postal_code=c.CUSTOMER_POSTAL_CODE,
                created_at=c.CREATED_AT,
                updated_at=c.UPDATED_AT
            ))
            
        return CustomersResponse(status=True, data=customers)
    except Exception as e:
        # Log the actual error in a real app
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
