from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc
from app.db.session import get_db
from app.models.invoice import Invoice
from app.schemas.dashboard import DashboardResponse, DashboardData, StatsSummary, ActivityPoint, CountryShare, DocTypeShare, RecentDocument
from typing import List, Optional
from datetime import datetime, timedelta
from urllib.parse import quote

router = APIRouter()

def get_file_url(request: Request, inv_doc_id: str, has_attachment: bool):
    if not has_attachment:
        return None
    # Use request.base_url for absolute URL and match the format in invoices.py
    base_url = str(request.base_url).rstrip("/")
    safe_doc_id = quote(inv_doc_id)
    return f"{base_url}/api/invoices/attachment?docId={safe_doc_id}"

@router.get("", response_model=DashboardResponse)
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    """Fetch dashboard analytics with optimized performance."""
    try:
        # 1. OPTIMIZED STATS: Get all counts in a single query using grouping
        status_counts = db.query(Invoice.STATUS, func.count(Invoice.DOC_ID)).group_by(Invoice.STATUS).all()
        counts_dict = dict(status_counts)
        
        pending = counts_dict.get("pending", 0)
        accepted = counts_dict.get("accepted", 0)
        rejected = counts_dict.get("rejected", 0)
        total_docs = sum(counts_dict.values())

        stats = StatsSummary(
            totalDocuments=total_docs,
            pending=pending,
            completed=accepted,
            rejected=rejected
        )

        # 2. OPTIMIZED RECENT DOCUMENTS: Exclude LargeBinary (FILE_CONTENT)
        stmt = select(
            Invoice.DOC_ID,
            Invoice.SOURCE_REFERENCE,
            Invoice.CUSTOMER_NAME,
            Invoice.GROSS_AMOUNT,
            Invoice.CREATED_AT,
            Invoice.STATUS,
            Invoice.DOC_TYPE,
            Invoice.HAS_ATTACHMENT
        ).order_by(desc(Invoice.CREATED_AT)).limit(5)
        
        db_recent = db.execute(stmt).all()
        recent_documents = [RecentDocument(
            docId=row.DOC_ID,
            sourceReference=row.SOURCE_REFERENCE or "",
            customer=row.CUSTOMER_NAME,
            grossAmount=f"{float(row.GROSS_AMOUNT):.2f}",
            created=row.CREATED_AT.strftime("%b %d, %Y"),
            status=row.STATUS,
            docType=row.DOC_TYPE,
            hasAttachment=row.HAS_ATTACHMENT,
            fileUrl=get_file_url(request, row.DOC_ID, row.HAS_ATTACHMENT)
        ) for row in db_recent]

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

        # 5. OPTIMIZED ACTIVITY DATA: Single query for last 7 days
        seven_days_ago = datetime.utcnow().date() - timedelta(days=6)
        activity_agg = db.query(
            func.date(Invoice.CREATED_AT).label('day'),
            func.count(Invoice.DOC_ID)
        ).filter(func.date(Invoice.CREATED_AT) >= seven_days_ago)\
         .group_by(func.date(Invoice.CREATED_AT))\
         .order_by('day').all()
        
        activity_dict = {day.strftime("%b %d"): count for day, count in activity_agg}
        
        activity_data = []
        for i in range(6, -1, -1):
            date = datetime.utcnow() - timedelta(days=i)
            date_str = date.strftime("%b %d")
            activity_data.append(ActivityPoint(
                date=date_str, 
                count=activity_dict.get(date_str, 0)
            ))

        data = DashboardData(
            stats=stats,
            activityData=activity_data,
            countryData=country_data,
            docDistribution=doc_distribution,
            recentDocuments=recent_documents
        )
        return DashboardResponse(status=True, data=data)
    except Exception as e:
        print(f"ERROR in dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
