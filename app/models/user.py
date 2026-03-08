from sqlalchemy import Column, String, DateTime, Boolean, JSON
from app.db.base_class import Base
from datetime import datetime

class User(Base):
    __tablename__ = "USERS"

    USER_ID = Column(String(50), primary_key=True, index=True)
    EMAIL = Column(String(255), unique=True, index=True, nullable=False)
    NAME = Column(String(255), nullable=False)
    CLIENT_NAME = Column(String(255), nullable=False)
    ADDRESS_LINE1 = Column(String(255), nullable=True)
    ADDRESS_LINE2 = Column(String(255), nullable=True)
    CITY = Column(String(50), nullable=True)
    STATE = Column(String(50), nullable=True)
    COUNTRY = Column(String(50), nullable=True)
    POSTAL_CODE = Column(String(20), nullable=True)
    BANK_NAME = Column(String(255), nullable=True)
    BANK_BENEFICIARY_NAME = Column(String(255), nullable=True)
    BANK_BENEFICIAL_ACCOUNT_NUMBER = Column(String(100), nullable=True)
    BANK_SWIFT_CODE = Column(String(50), nullable=True)
    BANK_IBAN = Column(String(100), nullable=True)
    BANK_CURRENCY = Column(String(10), nullable=True)
    # Storing roles as a comma-separated string or JSON based on HANA's flexibility
    ROLE_TYPE = Column(JSON, nullable=False, default=["USER"])
    STATUS = Column(String(20), default="ACTIVE")
    ALLOWED_COUNTRIES = Column(JSON, nullable=False, default=[])
    IS_PARTNER = Column(Boolean, default=False)
    AUTO_SUBMIT = Column(Boolean, default=True)
    API_KEY = Column(String(100), nullable=True)
    UPLOADS_ENABLED = Column(Boolean, default=True)
    LAST_LOGIN = Column(DateTime, nullable=True)
    CREATED_AT = Column(DateTime, default=datetime.utcnow)
    UPDATED_AT = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
