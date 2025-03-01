from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# # Get database URL from environment variables, or use a default
# DATABASE_URL = os.getenv(
#     "DATABASE_URL", 
#     "postgresql://postgres:postgres@localhost/url_shortener"
# )

# # Create SQLAlchemy engine
# engine = create_engine(DATABASE_URL)

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost/url_shortener"
)

# Append `?sslmode=require` if deploying on Render
if DATABASE_URL.startswith("postgresql://") and "localhost" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
