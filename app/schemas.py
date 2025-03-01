from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    original_url: str
    
    @validator("original_url")
    def validate_url(cls, v):
        # Basic URL validation - could be enhanced
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v

class URLCreate(URLBase):
    pass

class URL(URLBase):
    id: int
    short_url: str
    created_at: datetime
    is_active: bool
    clicks: int
    
    class Config:
        orm_mode = True

class URLStats(BaseModel):
    original_url: str
    short_url: str
    clicks: int
    created_at: datetime