from sqlalchemy import Column, String, DateTime
from app.db.base_class import Base
from datetime import datetime

class Customer(Base):
    # The __tablename__ will be automatically set to "CUSTOMER" 
    # based on the class name and our base class logic.
    # If the table is plural, we can manually override it:
    __tablename__ = "CUSTOMERS"

    ID = Column(String(50), primary_key=True, index=True)
    CUSTOMER_ID = Column(String(50), nullable=False)
    CUSTOMER_TAX_ID = Column(String(50), nullable=False)
    CUSTOMER_NAME = Column(String(255), nullable=False)
    CUSTOMER_EMAIL = Column(String(255), nullable=True)
    CUSTOMER_PHONE = Column(String(50), nullable=True)
    CUSTOMER_ADDRESS_LINE1 = Column(String(255), nullable=True)
    CUSTOMER_ADDRESS_LINE2 = Column(String(255), nullable=True)
    CUSTOMER_STATE = Column(String(50), nullable=True)
    CUSTOMER_COUNTRY_CODE = Column(String(10), nullable=False)
    CUSTOMER_POSTAL_CODE = Column(String(20), nullable=True)
    CREATED_AT = Column(DateTime, default=datetime.utcnow)
    UPDATED_AT = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
