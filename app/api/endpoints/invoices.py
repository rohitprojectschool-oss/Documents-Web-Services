from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.invoice import Invoice
import random
from datetime import datetime
from app.schemas.invoice import InvoicesResponse, Invoice as InvoiceSchema, InvoiceCreate, InvoiceResponse

router = APIRouter()

@router.get("", response_model=InvoicesResponse)
async def get_invoices(db: Session = Depends(get_db)):
    """Fetch all invoices from SAP HANA."""
    try:
        db_invoices = db.query(Invoice).all()
        invoices = [InvoiceSchema(
            docId=inv.DOC_ID,
            sourceReference=inv.SOURCE_REFERENCE or "",
            customer=inv.CUSTOMER_NAME,
            grossAmount=f"{float(inv.GROSS_AMOUNT):.2f}",
            created=inv.CREATED_AT.strftime("%b %d, %Y"),
            status=inv.STATUS,
            docType=inv.DOC_TYPE,
            countryCode=inv.COUNTRY_CODE,
            countryName=inv.COUNTRY_NAME
        ) for inv in db_invoices]
        return InvoicesResponse(status=True, data=invoices)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("", response_model=InvoiceResponse)
async def upload_invoice(invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    """Upload/Create a new invoice in SAP HANA."""
    try:
        # Generate a random DOC_ID similar to the existing format
        random_num = random.randint(100, 999)
        doc_id = f"FT {invoice_in.countryCode}{random.randint(1000, 9999)}S{random.randint(1000, 9999)}N/{random_num}"
        
        new_invoice = Invoice(
            DOC_ID=doc_id,
            SOURCE_REFERENCE=invoice_in.sourceReference,
            CUSTOMER_NAME=invoice_in.customer,
            GROSS_AMOUNT=invoice_in.grossAmount,
            STATUS="pending", # Default status
            DOC_TYPE=invoice_in.docType,
            COUNTRY_CODE=invoice_in.countryCode,
            COUNTRY_NAME=invoice_in.countryName,
            CREATED_AT=datetime.utcnow(),
            UPDATED_AT=datetime.utcnow()
        )
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)
        
        return InvoiceResponse(
            status=True,
            message="Invoice uploaded successfully",
            data=InvoiceSchema(
                docId=new_invoice.DOC_ID,
                sourceReference=new_invoice.SOURCE_REFERENCE or "",
                customer=new_invoice.CUSTOMER_NAME,
                grossAmount=f"{float(new_invoice.GROSS_AMOUNT):.2f}",
                created=new_invoice.CREATED_AT.strftime("%b %d, %Y"),
                status=new_invoice.STATUS,
                docType=new_invoice.DOC_TYPE,
                countryCode=new_invoice.COUNTRY_CODE,
                countryName=new_invoice.COUNTRY_NAME
            )
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload invoice: {str(e)}")
