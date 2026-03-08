from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.invoice import Invoice
from app.schemas.invoice import InvoicesResponse, Invoice as InvoiceSchema

router = APIRouter()

@router.get("", response_model=InvoicesResponse)
async def get_invoices(db: Session = Depends(get_db)):
    """Fetch all invoices from SAP HANA."""
    try:
        db_invoices = db.query(Invoice).all()
        
        invoices = []
        for inv in db_invoices:
            invoices.append(InvoiceSchema(
                docId=inv.DOC_ID,
                sourceReference=inv.SOURCE_REFERENCE or "",
                customer=inv.CUSTOMER_NAME,
                grossAmount=f"{float(inv.GROSS_AMOUNT):.2f}", # Simple string formatting
                created=inv.CREATED_AT.strftime("%b %d, %Y"),
                status=inv.STATUS,
                docType=inv.DOC_TYPE,
                countryCode=inv.COUNTRY_CODE,
                countryName=inv.COUNTRY_NAME
            ))
            
        return InvoicesResponse(status=True, data=invoices)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
