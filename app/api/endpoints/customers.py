from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.customer import Customer
import uuid
from datetime import datetime
from app.schemas.customer import CustomersResponse, Customer as CustomerSchema, CustomerCreate, CustomerResponse

router = APIRouter()

@router.get("", response_model=CustomersResponse)
async def get_customers(db: Session = Depends(get_db)):
    """Fetch all customers from SAP HANA."""
    try:
        db_customers = db.query(Customer).all()
        customers = [CustomerSchema(
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
        ) for c in db_customers]
        return CustomersResponse(status=True, data=customers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("", response_model=CustomerResponse)
async def create_customer(customer_in: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer in SAP HANA."""
    try:
        new_customer = Customer(
            ID=str(uuid.uuid4()),
            CUSTOMER_ID=customer_in.customer_id,
            CUSTOMER_TAX_ID=customer_in.customer_tax_id,
            CUSTOMER_NAME=customer_in.customer_name,
            CUSTOMER_EMAIL=customer_in.customer_email,
            CUSTOMER_PHONE=customer_in.customer_phone,
            CUSTOMER_ADDRESS_LINE1=customer_in.customer_address_line1,
            CUSTOMER_ADDRESS_LINE2=customer_in.customer_address_line2,
            CUSTOMER_STATE=customer_in.customer_state,
            CUSTOMER_COUNTRY_CODE=customer_in.customer_country_code,
            CUSTOMER_POSTAL_CODE=customer_in.customer_postal_code,
            CREATED_AT=datetime.utcnow(),
            UPDATED_AT=datetime.utcnow()
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        
        return CustomerResponse(
            status=True,
            message="Customer created successfully",
            data=CustomerSchema(
                id=new_customer.ID,
                customer_id=new_customer.CUSTOMER_ID,
                customer_tax_id=new_customer.CUSTOMER_TAX_ID,
                customer_name=new_customer.CUSTOMER_NAME,
                customer_email=new_customer.CUSTOMER_EMAIL,
                customer_phone=new_customer.CUSTOMER_PHONE,
                customer_address_line1=new_customer.CUSTOMER_ADDRESS_LINE1,
                customer_address_line2=new_customer.CUSTOMER_ADDRESS_LINE2,
                customer_state=new_customer.CUSTOMER_STATE,
                customer_country_code=new_customer.CUSTOMER_COUNTRY_CODE,
                customer_postal_code=new_customer.CUSTOMER_POSTAL_CODE,
                created_at=new_customer.CREATED_AT,
                updated_at=new_customer.UPDATED_AT
            )
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create customer: {str(e)}")
