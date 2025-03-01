from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import time

from . import models, schemas, utils
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="URL Shortener API")

@app.post("/api/shorten/", response_model=schemas.URL)
def create_short_url(url_data: schemas.URLCreate, db: Session = Depends(get_db)):
    """
    Create a shortened URL from the original URL.
    """
    # Validate URL (basic validation)
    if not utils.is_valid_url(url_data.original_url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    # Generate a short URL
    short_code = utils.generate_short_url(url_data.original_url)
    
    # Check if this short code already exists (collision)
    while db.query(models.URL).filter(models.URL.short_url == short_code).first():
        # Regenerate with a slightly different approach to avoid collision
        short_code = utils.generate_short_url(url_data.original_url + str(time.time()))
    
    # Create URL object
    db_url = models.URL(
        original_url=url_data.original_url,
        short_url=short_code,
    )
    
    # Save to database
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return db_url

@app.get("/{short_url}")
def redirect_to_original(short_url: str, db: Session = Depends(get_db)):
    """
    Redirect from the short URL to the original URL.
    """
    # Find the URL in the database
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    
    # Check if URL exists
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Check if URL is active
    if not db_url.is_active:
        raise HTTPException(status_code=410, detail="URL has been deactivated")
    
    # Increment the click count
    db_url.clicks += 1
    db.commit()
    
    # Redirect to the original URL
    return RedirectResponse(url=db_url.original_url)

@app.get("/api/stats/{short_url}", response_model=schemas.URLStats)
def get_url_stats(short_url: str, db: Session = Depends(get_db)):
    """
    Get statistics for a shortened URL.
    """
    # Find the URL in the database
    db_url = db.query(models.URL).filter(models.URL.short_url == short_url).first()
    
    # Check if URL exists
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return schemas.URLStats(
        original_url=db_url.original_url,
        short_url=db_url.short_url,
        clicks=db_url.clicks,
        created_at=db_url.created_at
    )

@app.get("/api/urls/", response_model=List[schemas.URL])
def get_all_urls(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Get all URLs with pagination.
    """
    urls = db.query(models.URL).offset(skip).limit(limit).all()
    return urls