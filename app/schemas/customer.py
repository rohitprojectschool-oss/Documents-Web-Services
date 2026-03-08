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

class CustomersResponse(BaseModel):
    status: bool
    data: List[Customer]
