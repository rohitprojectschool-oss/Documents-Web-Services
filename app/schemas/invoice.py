from typing import List, Optional
from pydantic import BaseModel

class Invoice(BaseModel):
    docId: str
    sourceReference: str
    customer: str
    grossAmount: str
    created: str
    status: str
    docType: str
    countryCode: str
    countryName: str

class InvoiceCreate(BaseModel):
    sourceReference: str
    customer: str
    grossAmount: float
    docType: str
    countryCode: str
    countryName: str

class InvoiceResponse(BaseModel):
    status: bool
    message: str
    data: Optional[Invoice] = None

class InvoicesResponse(BaseModel):
    status: bool
    data: List[Invoice]
