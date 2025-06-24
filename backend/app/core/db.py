from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.settings import settings
from sqlalchemy.ext.declarative import declarative_base

# Create the SQLAlchemy Engine using the Database URL from settings.py
DATABASE_URL = settings.DATABASE_URL

# Create an Engine Instance
engine = create_engine(DATABASE_URL, echo=True)

# Create a Sessionmaker
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind=engine
)

# Base Class for any models to inherit from - to be recognized and mapped to tables.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        print("Database session created")
        yield db
    finally:
        db.close()