from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class UserProfile(BaseModel):
    user_id: str
    email: str
    name: str
    client_name: str
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    bank_name: Optional[str] = None
    bank_beneficiary_name: Optional[str] = None
    bank_beneficial_account_number: Optional[str] = None
    bank_swift_code: Optional[str] = None
    bank_iban: Optional[str] = None
    bank_currency: Optional[str] = None
    role_type: List[str]
    status: str
    allowed_countries: List[str]
    is_partner: bool
    auto_submit: bool
    api_key: str
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    uploads_enabled: bool
    environment_preference: Optional[str] = None
    has_brand_logo: bool

class AuthMeResponse(BaseModel):
    success: bool
    message: str
    data: UserProfile
