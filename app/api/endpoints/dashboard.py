from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.invoice import Invoice
from app.schemas.dashboard import DashboardResponse, DashboardData, StatsSummary, ActivityPoint, CountryShare, DocTypeShare, RecentDocument
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

def get_file_url(request: Request, inv: Invoice):
    if not inv.HAS_ATTACHMENT or not inv.FILE_CONTENT:
        return None
    base_url = str(request.base_url).rstrip("/")
    return f"{base_url}/api/invoices/{inv.DOC_ID}/file"

@router.get("", response_model=DashboardResponse)
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    """Fetch real-time dashboard analytics."""
    try:
        # 1. Calculate Stats Summary
        total_docs = db.query(Invoice).count()
        pending = db.query(Invoice).filter(Invoice.STATUS == "pending").count()
        accepted = db.query(Invoice).filter(Invoice.STATUS == "accepted").count()
        rejected = db.query(Invoice).filter(Invoice.STATUS == "rejected").count()

        stats = StatsSummary(
            totalDocuments=total_docs,
            pending=pending,
            completed=accepted,
            rejected=rejected
        )

        # 2. Fetch Recent Documents (limit to 5)
        db_recent = db.query(Invoice).order_by(Invoice.CREATED_AT.desc()).limit(5).all()
        recent_documents = []
        for inv in db_recent:
            recent_documents.append(RecentDocument(
                docId=inv.DOC_ID,
                sourceReference=inv.SOURCE_REFERENCE or "",
                customer=inv.CUSTOMER_NAME,
                grossAmount=f"{float(inv.GROSS_AMOUNT):.2f}",
                created=inv.CREATED_AT.strftime("%b %d, %Y"),
                status=inv.STATUS,
                docType=inv.DOC_TYPE,
                hasAttachment=inv.HAS_ATTACHMENT and inv.FILE_CONTENT is not None,
                fileUrl=get_file_url(request, inv)
            ))

        # 3. Country Distribution
        country_agg = db.query(
            Invoice.COUNTRY_NAME, 
            func.count(Invoice.DOC_ID)
        ).group_by(Invoice.COUNTRY_NAME).all()
        
        country_data = []
        colors = ['#e53e3e', '#4299e1', '#48bb78', '#ecc94b']
        for i, (name, count) in enumerate(country_agg):
            percentage = round((count / total_docs) * 100) if total_docs > 0 else 0
            country_data.append(CountryShare(
                name=name,
                value=percentage,
                color=colors[i % len(colors)]
            ))

        # 4. Doc Type Distribution
        type_agg = db.query(
            Invoice.DOC_TYPE, 
            func.count(Invoice.DOC_ID)
        ).group_by(Invoice.DOC_TYPE).all()
        
        doc_distribution = []
        for i, (doc_type, count) in enumerate(type_agg):
            percentage = round((count / total_docs) * 100) if total_docs > 0 else 0
            doc_distribution.append(DocTypeShare(
                type=doc_type,
                percentage=percentage,
                color=colors[i % len(colors)]
            ))

        # 5. Activity Data (Last 7 days)
        activity_data = []
        for i in range(6, -1, -1):
            date = datetime.utcnow() - timedelta(days=i)
            date_str = date.strftime("%b %d")
            
            count = db.query(Invoice).filter(
                func.date(Invoice.CREATED_AT) == date.date()
            ).count()
            
            activity_data.append(ActivityPoint(date=date_str, count=count))

        data = DashboardData(
            stats=stats,
            activityData=activity_data,
            countryData=country_data,
            docDistribution=doc_distribution,
            recentDocuments=recent_documents
        )
        return DashboardResponse(status=True, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
