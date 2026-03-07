import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./scan_history.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ScanResult(Base):
    __tablename__ = "scans"

    scan_id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    confidence = Column(Float)
    result_label = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    explanation_json = Column(Text)  # Storing as JSON string to stay simple with SQLite

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
