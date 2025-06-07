from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from datetime import datetime

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zillow_id = Column(String, unique=True, index=True)
    address = Column(String, nullable=False)
    location = Column(Geometry('POINT'), nullable=False)
    zillow_url = Column(String)
    image_url = Column(String)
    price = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class SearchLog(Base):
    __tablename__ = "search_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_image_url = Column(String)
    search_location = Column(Geometry('POINT'))
    matched_property_id = Column(UUID(as_uuid=True))
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow) 