import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Legacy psycopg2 connection for raw SQL (keep for compatibility)
def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Database model
class Delivery(Base):
    __tablename__ = "deliveries"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    perishability = Column(Integer)
    travel_time_sec = Column(Integer)
    weather = Column(String)
    final_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)