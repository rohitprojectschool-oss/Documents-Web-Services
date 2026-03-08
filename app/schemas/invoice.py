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

class InvoicesResponse(BaseModel):
    status: bool
    data: List[Invoice]
