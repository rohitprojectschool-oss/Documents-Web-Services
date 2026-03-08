from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.db.session import get_db
from app.models.invoice import Invoice
from app.schemas.analytics import AnalyticsResponse, AnalyticsData, CountryStat, MonthlyTrend, DocTypeStat

router = APIRouter()

@router.get("", response_model=AnalyticsResponse)
async def get_analytics(db: Session = Depends(get_db)):
    """Fetch real-time analytics aggregations from SAP HANA."""
    try:
        # 1. KPI Calculations
        total_docs = db.query(Invoice).count()
        if total_docs == 0:
            return AnalyticsResponse(status=True, data=AnalyticsData(
                totalDocuments=0, acceptanceRate=0, rejectionRate=0, activeCountries=0,
                countryStats=[], monthlyTrends=[], docTypeStats=[]
            ))

        accepted_docs = db.query(Invoice).filter(Invoice.STATUS == "accepted").count()
        rejected_docs = db.query(Invoice).filter(Invoice.STATUS == "rejected").count()
        active_countries_count = db.query(func.count(func.distinct(Invoice.COUNTRY_CODE))).scalar()

        acceptance_rate = round((accepted_docs / total_docs) * 100) if total_docs > 0 else 0
        rejection_rate = round((rejected_docs / total_docs) * 100) if total_docs > 0 else 0

        # 2. Country Stats (Table breakdown)
        # Using sqlalchemy.case instead of func.case
        country_agg = db.query(
            Invoice.COUNTRY_CODE,
            Invoice.COUNTRY_NAME,
            func.count(Invoice.DOC_ID).label('total'),
            func.sum(case((Invoice.STATUS == 'accepted', 1), else_=0)).label('accepted'),
            func.sum(case((Invoice.STATUS == 'rejected', 1), else_=0)).label('rejected'),
            func.sum(case((Invoice.STATUS == 'pending', 1), else_=0)).label('pending')
        ).group_by(Invoice.COUNTRY_CODE, Invoice.COUNTRY_NAME).all()

        country_stats = [
            CountryStat(
                countryCode=row.COUNTRY_CODE,
                countryName=row.COUNTRY_NAME,
                total=int(row.total or 0),
                accepted=int(row.accepted or 0),
                rejected=int(row.rejected or 0),
                pending=int(row.pending or 0)
            ) for row in country_agg
        ]

        # 3. Monthly Trends
        # For SAP HANA, we use MONTHNAME or similar. 
        # Using a subquery/label approach for grouping.
        month_label = func.monthname(Invoice.CREATED_AT).label('month')
        monthly_agg = db.query(
            month_label,
            Invoice.COUNTRY_CODE,
            func.count(Invoice.DOC_ID).label('count')
        ).group_by(month_label, Invoice.COUNTRY_CODE).all()

        trends_map = {}
        for row in monthly_agg:
            # Format month to 3 chars if needed (e.g. "January" -> "Jan")
            m = row.month[:3] if row.month else "Unk"
            if m not in trends_map:
                trends_map[m] = {"month": m}
            trends_map[m][row.COUNTRY_CODE] = int(row.count)
        
        monthly_trends = [MonthlyTrend(**v) for v in trends_map.values()]

        # 4. Doc Type Breakdown
        type_agg = db.query(
            Invoice.DOC_TYPE,
            func.count(Invoice.DOC_ID).label('count')
        ).group_by(Invoice.DOC_TYPE).all()

        colors = ['#e53e3e', '#4299e1', '#718096', '#ecc94b']
        doc_type_stats = [
            DocTypeStat(
                type=row.DOC_TYPE,
                count=int(row.count),
                color=colors[i % len(colors)]
            ) for i, row in enumerate(type_agg)
        ]

        data = AnalyticsData(
            totalDocuments=total_docs,
            acceptanceRate=acceptance_rate,
            rejectionRate=rejection_rate,
            activeCountries=active_countries_count,
            countryStats=country_stats,
            monthlyTrends=monthly_trends,
            docTypeStats=doc_type_stats
        )

        return AnalyticsResponse(status=True, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")
