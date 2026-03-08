from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the SQLAlchemy engine for SAP HANA
# Connect to the HANA database using the provided URL
engine = create_engine(
    settings.HANA_URL,
    echo=True, # Log SQL queries for development
    pool_size=10,
    max_overflow=20
)

# Create a "SessionLocal" class
# This will be used to create actual database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for getting a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
