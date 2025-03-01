from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from .database import Base

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_url = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<URL(original_url='{self.original_url}', short_url='{self.short_url}')>"