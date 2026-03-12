from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.invoice import Invoice
import random
from datetime import datetime
from app.schemas.invoice import InvoicesResponse, Invoice as InvoiceSchema, InvoiceResponse
from urllib.parse import quote, unquote

router = APIRouter()

def get_file_url(inv_doc_id: str, has_attachment: bool):
    if not has_attachment:
        return None
    # Use a relative URL. The frontend will prepend the correct BASE_URL.
    # This prevents the "localhost" issue in production.
    safe_doc_id = quote(inv_doc_id, safe='/')
    return f"/api/invoices/{safe_doc_id}/file"

@router.get("/{doc_id:path}/file")
async def download_document(doc_id: str, db: Session = Depends(get_db)):
    """Serve document content directly from DB using the path-based URL."""
    # Try direct match
    inv = db.query(Invoice).filter(Invoice.DOC_ID == doc_id).first()
    
    # If not found, it might be double-encoded in the URL
    if not inv and '%' in doc_id:
        decoded_id = unquote(doc_id)
        inv = db.query(Invoice).filter(Invoice.DOC_ID == decoded_id).first()
    
    if not inv:
        raise HTTPException(status_code=404, detail=f"Invoice record '{doc_id}' not found")
    
    if not inv.FILE_CONTENT:
        raise HTTPException(status_code=404, detail="File content missing")
    
    # SANITIZATION: HTTP headers only support latin-1 characters. 
    original_filename = inv.FILE_NAME or "document"
    ascii_filename = original_filename.encode('ascii', 'ignore').decode('ascii') or "document"
    filename_quoted = quote(original_filename)
    
    return Response(
        content=inv.FILE_CONTENT,
        media_type=inv.FILE_MIME_TYPE or "application/octet-stream",
        headers={
            "Content-Disposition": f"inline; filename=\"{ascii_filename}\"; filename*=UTF-8''{filename_quoted}"
        }
    )

@router.get("", response_model=InvoicesResponse)
async def get_invoices(db: Session = Depends(get_db)):
    """Fetch all invoices from DB efficiently."""
    try:
        # PERFORMANCE FIX: We EXCLUDE FILE_CONTENT from the list query.
        # Fetching 7MB blobs for every row in a list is what makes it "notoriously slow".
        stmt = select(
            Invoice.DOC_ID,
            Invoice.SOURCE_REFERENCE,
            Invoice.CUSTOMER_NAME,
            Invoice.GROSS_AMOUNT,
            Invoice.CREATED_AT,
            Invoice.STATUS,
            Invoice.DOC_TYPE,
            Invoice.COUNTRY_CODE,
            Invoice.COUNTRY_NAME,
            Invoice.HAS_ATTACHMENT
        )
        results = db.execute(stmt).all()
        
        invoices = [InvoiceSchema(
            docId=row.DOC_ID,
            sourceReference=row.SOURCE_REFERENCE or "",
            customer=row.CUSTOMER_NAME,
            grossAmount=f"{float(row.GROSS_AMOUNT):.2f}",
            created=row.CREATED_AT.strftime("%b %d, %Y"),
            status=row.STATUS,
            docType=row.DOC_TYPE,
            countryCode=row.COUNTRY_CODE,
            countryName=row.COUNTRY_NAME,
            hasAttachment=row.HAS_ATTACHMENT,
            fileUrl=get_file_url(row.DOC_ID, row.HAS_ATTACHMENT)
        ) for row in results]
        
        return InvoicesResponse(status=True, data=invoices)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("", response_model=InvoiceResponse)
async def upload_invoice(
    sourceReference: str = Form(...),
    customer: str = Form(...),
    grossAmount: float = Form(...),
    docType: str = Form(...),
    countryCode: str = Form(...),
    countryName: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload/Create a new invoice with file storage in DB."""
    try:
        content = await file.read()
        
        # Generate a random DOC_ID
        random_num = random.randint(100, 999)
        doc_id = f"FT {countryCode}{random.randint(1000, 9999)}S{random.randint(1000, 9999)}N/{random_num}"
        
        new_invoice = Invoice(
            DOC_ID=doc_id,
            SOURCE_REFERENCE=sourceReference,
            CUSTOMER_NAME=customer,
            GROSS_AMOUNT=grossAmount,
            STATUS="pending",
            DOC_TYPE=docType,
            COUNTRY_CODE=countryCode,
            COUNTRY_NAME=countryName or "Angola",
            HAS_ATTACHMENT=True,
            FILE_CONTENT=content,
            FILE_NAME=file.filename,
            FILE_MIME_TYPE=file.content_type,
            CREATED_AT=datetime.utcnow()
        )
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)
        
        return InvoiceResponse(
            status=True,
            message=f"Invoice {file.filename} stored in database successfully",
            data=InvoiceSchema(
                docId=new_invoice.DOC_ID,
                sourceReference=new_invoice.SOURCE_REFERENCE or "",
                customer=new_invoice.CUSTOMER_NAME,
                grossAmount=f"{float(new_invoice.GROSS_AMOUNT):.2f}",
                created=new_invoice.CREATED_AT.strftime("%b %d, %Y"),
                status=new_invoice.STATUS,
                docType=new_invoice.DOC_TYPE,
                countryCode=new_invoice.COUNTRY_CODE,
                countryName=new_invoice.COUNTRY_NAME,
                hasAttachment=True,
                fileUrl=get_file_url(new_invoice.DOC_ID, True)
            )
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload invoice: {str(e)}")
