from sqlalchemy import Column, String, DateTime, Numeric, Boolean, LargeBinary
from app.db.base_class import Base
from datetime import datetime

class Invoice(Base):
    __tablename__ = "INVOICES"

    DOC_ID = Column(String(100), primary_key=True, index=True)
    SOURCE_REFERENCE = Column(String(100), nullable=True)
    CUSTOMER_NAME = Column(String(255), nullable=False)
    # Using Numeric for gross amount to handle financial calculations properly
    GROSS_AMOUNT = Column(Numeric(18, 2), nullable=False)
    STATUS = Column(String(50), nullable=False) # e.g., 'accepted', 'rejected', 'pending'
    DOC_TYPE = Column(String(100), nullable=False) # e.g., 'Standard Invoice'
    COUNTRY_CODE = Column(String(10), nullable=False)
    COUNTRY_NAME = Column(String(100), nullable=False)
    HAS_ATTACHMENT = Column(Boolean, default=False)
    FILE_CONTENT = Column(LargeBinary, nullable=True)
    FILE_NAME = Column(String(255), nullable=True)
    FILE_MIME_TYPE = Column(String(100), nullable=True)
    CREATED_AT = Column(DateTime, default=datetime.utcnow)
    UPDATED_AT = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
