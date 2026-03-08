from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SettingsSaveRequest(BaseModel):
    # Add fields based on what frontend sends
    name: str
    email: str
    nif: str
    address: str

@router.post("/save")
async def save_settings(request: SettingsSaveRequest):
    return {"status": True, "message": "Settings saved successfully"}

@router.post("/change-password")
async def change_password():
    return {"status": True, "message": "Password changed successfully"}

@router.post("/generate-api-key")
async def generate_api_key():
    return {"status": True, "data": {"api_key": "pk_new_key_12345"}}
