from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import AuthMeResponse, UserProfile

router = APIRouter()

@router.get("/me", response_model=AuthMeResponse)
async def get_me(db: Session = Depends(get_db)):
    """Fetch current user profile from SAP HANA."""
    try:
        # For now, we fetch a fixed user ID to match the previous mock
        # In a real app, this would come from a JWT token or session
        user_id = "d8b00da2-b84f-41d7-bc6f-b0bde022243a"
        db_user = db.query(User).filter(User.USER_ID == user_id).first()
        
        if not db_user:
            # Fallback or error if user doesn't exist in DB yet
            raise HTTPException(status_code=404, detail="User not found")

        user_profile = UserProfile(
            user_id=db_user.USER_ID,
            email=db_user.EMAIL,
            name=db_user.NAME,
            client_name=db_user.CLIENT_NAME,
            address_line1=db_user.ADDRESS_LINE1,
            address_line2=db_user.ADDRESS_LINE2,
            city=db_user.CITY,
            state=db_user.STATE,
            country=db_user.COUNTRY,
            postal_code=db_user.POSTAL_CODE,
            bank_name=db_user.BANK_NAME,
            bank_beneficiary_name=db_user.BANK_BENEFICIARY_NAME,
            bank_beneficial_account_number=db_user.BANK_BENEFICIAL_ACCOUNT_NUMBER,
            bank_swift_code=db_user.BANK_SWIFT_CODE,
            bank_iban=db_user.BANK_IBAN,
            bank_currency=db_user.BANK_CURRENCY,
            role_type=db_user.ROLE_TYPE,
            status=db_user.STATUS,
            allowed_countries=db_user.ALLOWED_COUNTRIES,
            is_partner=db_user.IS_PARTNER,
            auto_submit=db_user.AUTO_SUBMIT,
            api_key=db_user.API_KEY or "",
            last_login=db_user.LAST_LOGIN,
            created_at=db_user.CREATED_AT,
            updated_at=db_user.UPDATED_AT,
            uploads_enabled=db_user.UPLOADS_ENABLED,
            has_brand_logo=False # Placeholder
        )
        return AuthMeResponse(success=True, message="ok", data=user_profile)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
