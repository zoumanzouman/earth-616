from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///./facilities.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI()

# Define the Facility database model
class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    contact = Column(String)
    hours = Column(String)
    category = Column(String)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request body and response validation
class FacilityBase(BaseModel):
    name: str
    location: str
    contact: str
    hours: str
    category: str

class FacilityCreate(FacilityBase):
    pass

class FacilityResponse(FacilityBase):
    id: int

    class Config:
        orm_mode = True


# API Endpoints

# Create a new facility
@app.post("/facilities/", response_model=FacilityResponse)
def create_facility(facility: FacilityCreate, db=Depends(get_db)):
    db_facility = Facility(**facility.dict())
    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility


# Get facilities by category
@app.get("/facilities/{category}", response_model=list[FacilityResponse])
def get_facilities_by_category(category: str, db=Depends(get_db)):
    facilities = db.query(Facility).filter(Facility.category == category).all()
    if not facilities:
        raise HTTPException(status_code=404, detail=f"No facilities found for {category}")
    return facilities


# Get all facilities (optional for testing)
@app.get("/facilities/", response_model=list[FacilityResponse])
def get_all_facilities(db=Depends(get_db)):
    return db.query(Facility).all()
