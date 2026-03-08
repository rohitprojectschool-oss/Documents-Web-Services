from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.country import Country
from app.schemas.country import CountrySettingsResponse, CountrySettingsData, Country as CountrySchema

router = APIRouter()

@router.get("/public", response_model=CountrySettingsResponse)
async def get_public_countries(db: Session = Depends(get_db)):
    """Fetch all public country settings from SAP HANA."""
    try:
        db_countries = db.query(Country).order_by(Country.DISPLAY_ORDER).all()
        
        countries = []
        for c in db_countries:
            countries.append(CountrySchema(
                country_code=c.COUNTRY_CODE,
                country_name=c.COUNTRY_NAME,
                flag_emoji=c.FLAG_EMOJI,
                display_order=c.DISPLAY_ORDER,
                region=c.REGION
            ))
            
        data = CountrySettingsData(
            countries=countries,
            sort_mode="alphabetical",
            use_only_configured=True,
            show_empty_countries=False
        )
        return CountrySettingsResponse(status=True, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
