from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import logging
import os
from datetime import datetime
import uuid

from app.models.database import Base, Property, SearchLog
from app.services.image_service import ImageService
from app.services.location_service import LocationService
from app.services.zillow_service import ZillowService
from app.database import get_db, engine
from app.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="House Finder API",
    description="API for finding houses from photos using computer vision",
    version="1.0.0"
)

# Load settings
settings = Settings()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
image_service = ImageService()
location_service = LocationService()
zillow_service = ZillowService(settings.ZILLOW_API_KEY)

@app.post("/api/v1/analyze-house")
async def analyze_house(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    db: Session = Depends(get_db)
):
    """Analyze a house photo and return matching property information"""
    try:
        # Save uploaded image
        image_path = f"uploads/{uuid.uuid4()}.jpg"
        os.makedirs("uploads", exist_ok=True)
        
        with open(image_path, "wb") as f:
            content = await image.read()
            f.write(content)
        
        # Extract location from EXIF if not provided
        if latitude is None or longitude is None:
            location = image_service.extract_location_from_exif(image_path)
            if location:
                latitude, longitude = location
            else:
                raise HTTPException(status_code=400, detail="Location data required")
        
        # Validate coordinates
        if not location_service.validate_coordinates(latitude, longitude):
            raise HTTPException(status_code=400, detail="Invalid coordinates")
        
        # Get nearby properties
        nearby_properties = location_service.get_nearby_properties(db, latitude, longitude)
        
        if not nearby_properties:
            # If no properties in database, fetch from Zillow
            zillow_properties = await zillow_service.search_properties_by_location(
                latitude, longitude
            )
            # Save new properties to database
            for prop_data in zillow_properties:
                property = zillow_service.parse_property_data(prop_data)
                db.add(property)
            db.commit()
            nearby_properties = location_service.get_nearby_properties(db, latitude, longitude)
        
        # Extract features from uploaded image
        uploaded_features = image_service.extract_image_features(image_path)
        
        # Find best match
        best_match = None
        best_score = -1
        
        for property in nearby_properties:
            if property.image_url:
                # Download and process property image
                property_image_path = f"uploads/property_{property.id}.jpg"
                # TODO: Download image from property.image_url
                
                # Calculate similarity
                property_features = image_service.extract_image_features(property_image_path)
                similarity = image_service.calculate_similarity(
                    uploaded_features, property_features
                )
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = property
        
        if not best_match:
            raise HTTPException(status_code=404, detail="No matching property found")
        
        # Log search
        search_log = SearchLog(
            user_image_url=image_path,
            search_location=location_service.create_point(latitude, longitude),
            matched_property_id=best_match.id,
            confidence_score=best_score
        )
        db.add(search_log)
        db.commit()
        
        # Clean up uploaded files in background
        background_tasks.add_task(os.remove, image_path)
        
        return {
            "property": {
                "id": str(best_match.id),
                "address": best_match.address,
                "price": best_match.price,
                "bedrooms": best_match.bedrooms,
                "bathrooms": best_match.bathrooms,
                "zillow_url": best_match.zillow_url,
                "image_url": best_match.image_url
            },
            "confidence_score": best_score
        }
        
    except Exception as e:
        logger.error(f"Error analyzing house: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/property/{property_id}")
async def get_property_details(
    property_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed property information"""
    try:
        property = db.query(Property).filter(Property.id == property_id).first()
        if not property:
            raise HTTPException(status_code=404, detail="Property not found")
        
        return {
            "id": str(property.id),
            "address": property.address,
            "price": property.price,
            "bedrooms": property.bedrooms,
            "bathrooms": property.bathrooms,
            "zillow_url": property.zillow_url,
            "image_url": property.image_url,
            "created_at": property.created_at
        }
    except Exception as e:
        logger.error(f"Error getting property details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 