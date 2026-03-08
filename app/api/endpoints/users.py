from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class User(BaseModel):
    id: str
    name: str
    email: str
    role: str
    status: str

@router.get("", response_model=List[User])
async def get_users():
    return [
        User(id="1", name="Admin User", email="admin@test.com", role="ADMIN", status="ACTIVE"),
        User(id="2", name="Standard User", email="user@test.com", role="USER", status="ACTIVE"),
    ]
