from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .models import end_of_year

class User(BaseModel):
    username : str
    password : str

class ShowUser(BaseModel):
    username : str
    
    class Config():
        from_attributes = True

class PoklonBon(BaseModel):
    barcode: str
    value: float
    status: Optional[str] = None
    customer_name: str
    #expires_at: Optional[datetime] = end_of_year
    expires_at: Optional[datetime] = Field(default_factory=end_of_year)

class ShowBon(BaseModel):
    barcode: str
    value: float
    status: Optional[str] = None
    customer_name: str
    creator: ShowUser
    #expires_at: Optional[datetime] = end_of_year
    expires_at: Optional[datetime] = Field(default_factory=end_of_year)

    model_config = {
        "from_attributes": True  # Omogućava konverziju iz SQLAlchemy modela
    }

class UpdateBon(BaseModel):
    barcode: Optional[str] = None
    value: Optional[float] = None
    expires_at: Optional[datetime] = None
    status: Optional[str] = None
    customer_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None