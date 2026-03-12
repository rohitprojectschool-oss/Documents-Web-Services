from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.invoice import Invoice
import random
from datetime import datetime
from typing import Optional
from app.schemas.invoice import InvoicesResponse, Invoice as InvoiceSchema, InvoiceResponse
from urllib.parse import quote, unquote

router = APIRouter()

def get_file_url(request: Request, inv_doc_id: str, has_attachment: bool):
    if not has_attachment:
        return None
    # Use request.base_url to ensure the URL is absolute and matches the backend's address.
    # We use a query parameter for docId because it's much safer than path parameters when IDs contain slashes.
    base_url = str(request.base_url).rstrip("/")
    safe_doc_id = quote(inv_doc_id)
    return f"{base_url}/api/invoices/attachment?docId={safe_doc_id}"

@router.get("/attachment")
async def download_document(docId: str, db: Session = Depends(get_db)):
    """Serve document content directly from DB using the docId query parameter."""
    # docId is already unquoted by FastAPI for query parameters
    inv = db.query(Invoice).filter(Invoice.DOC_ID == docId).first()
    
    if not inv:
        raise HTTPException(status_code=404, detail=f"Invoice record '{docId}' not found")
    
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
async def get_invoices(
    request: Request, 
    status: Optional[str] = None,
    countryCode: Optional[str] = None,
    docType: Optional[str] = None,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Fetch invoices from DB with filtering."""
    try:
        # PERFORMANCE FIX: We EXCLUDE FILE_CONTENT from the list query.
        query = select(
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

        # Apply Filters
        if status:
            query = query.where(Invoice.STATUS == status)
        if countryCode:
            query = query.where(Invoice.COUNTRY_CODE == countryCode)
        if docType:
            query = query.where(Invoice.DOC_TYPE == docType)
        if startDate:
            try:
                start_dt = datetime.strptime(startDate, "%Y-%m-%d")
                query = query.where(Invoice.CREATED_AT >= start_dt)
            except ValueError:
                pass # Or raise error
        if endDate:
            try:
                end_dt = datetime.strptime(endDate, "%Y-%m-%d")
                # Include the full end day
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
                query = query.where(Invoice.CREATED_AT <= end_dt)
            except ValueError:
                pass

        # Order by newest first
        query = query.order_by(Invoice.CREATED_AT.desc())
        
        results = db.execute(query).all()
        
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
            fileUrl=get_file_url(request, row.DOC_ID, row.HAS_ATTACHMENT)
        ) for row in results]
        
        return InvoicesResponse(status=True, data=invoices)
    except Exception as e:
        print(f"ERROR in get_invoices: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("", response_model=InvoiceResponse)
async def upload_invoice(
    request: Request,
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
                fileUrl=get_file_url(request, new_invoice.DOC_ID, True)
            )
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload invoice: {str(e)}")
