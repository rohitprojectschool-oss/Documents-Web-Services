from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    id: str
    customer_id: str
    customer_tax_id: str
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address_line1: Optional[str] = None
    customer_address_line2: Optional[str] = None
    customer_state: Optional[str] = None
    customer_country_code: str
    customer_postal_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CustomerCreate(BaseModel):
    customer_id: str
    customer_tax_id: str
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address_line1: Optional[str] = None
    customer_address_line2: Optional[str] = None
    customer_state: Optional[str] = None
    customer_country_code: str
    customer_postal_code: Optional[str] = None

class CustomerUpdate(BaseModel):
    customer_id: Optional[str] = None
    customer_tax_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address_line1: Optional[str] = None
    customer_address_line2: Optional[str] = None
    customer_state: Optional[str] = None
    customer_country_code: Optional[str] = None
    customer_postal_code: Optional[str] = None

class CustomerResponse(BaseModel):
    status: bool
    message: str
    data: Optional[Customer] = None

class CustomersResponse(BaseModel):
    status: bool
    data: List[Customer]
