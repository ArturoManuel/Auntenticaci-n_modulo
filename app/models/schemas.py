from pydantic import BaseModel, Field
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    rol: str
    
class UserLogin(BaseModel):
    username: str
    password: str




class TokenCreateRequest(BaseModel):
    user_id: int = Field(..., description="ID del usuario")

class TokenResponse(BaseModel):
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime
    status: bool
