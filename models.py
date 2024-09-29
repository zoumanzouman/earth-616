from sqlalchemy import Column, Integer, String
from database import Base

# Restaurants Model
class Restaurant(Base):
    __tablename__ = 'Restaurants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact = Column(String, nullable=False)

# Hospitals Model
class Hospital(Base):
    __tablename__ = 'Hospitals'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact = Column(String, nullable=False)

# Shops Model
class Shop(Base):
    __tablename__ = 'Shops'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact = Column(String)

# Places to Visit Model
class PlaceToVisit(Base):
    __tablename__ = 'PlacesToVisit'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
