from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Update with your actual PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:password@localhost:5432/brand_intelligence"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Mention(Base):
    __tablename__ = "mentions"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    relevance_score = Column(Float)
    matched_category = Column(String, index=True)
    confidence = Column(String)
    decision = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
