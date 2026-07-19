from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base

DATABASE_URL = "postgresql+psycopg://postgres:Mypost%40123@localhost:5432/codesage_ai"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()