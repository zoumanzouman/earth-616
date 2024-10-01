from fastapi.staticfiles import StaticFiles
import models
from database import engine, SessionLocal, get_db
from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Template setup
templates = Jinja2Templates(directory="frontend")

# Middleware for CORS
origins = ["http://127.0.0.1:8000/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint for homepage
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request): 
    return templates.TemplateResponse("html.html", {"request": request})

print('test point 1')



# Endpoint for searching facilities
@app.get("/search", response_class=HTMLResponse)
async def search_facilities(request: Request, query: str = None, db: Session = Depends(get_db)):
    search_results = []
    
    #: Log the received query
    print(f"Search query received: {query}")

    if query:
        query = query.strip()  # Remove unnecessary spaces

        # Search across all models using ilike for case-insensitive matching
        for model in [models.Restaurant, models.Hospital, models.Shop, models.PlaceToVisit]:
            facilities = db.query(model).filter(model.name.ilike(f"%{query}%")).all()
            if facilities:
                for facility in facilities:
                    search_results.append({
                        "name": facility.name,
                        "location": facility.location,
                        "contact": getattr(facility, "contact", None),
                        "category": model.__name__  # Optional: Add category for clarity
                    })
    
    # : Log the search results
    print(f"Facilities found: {search_results}")

    return templates.TemplateResponse("html.html", {
        "request": request, 
        "facilities": search_results if search_results else None,
        "error": "No facilities found." if not search_results else None
    })

print('test point2')

# Endpoint for fetching facilities by category
@app.get("/{category}", response_class=HTMLResponse)
async def get_facilities(request: Request, category: str, db: Session = Depends(get_db)):
    category_map = {
        "restaurants": models.Restaurant, 
        "shops": models.Shop,
        "hospitals": models.Hospital,
        "places_to_visit": models.PlaceToVisit
    }

    if category.lower() in category_map:
        model = category_map[category.lower()]
        facilities = db.query(model).all()

        facilities_list = [{"name": facility.name, "location": facility.location, "contact": getattr(facility, "contact", None)} for facility in facilities]

        return templates.TemplateResponse("html.html", {
            "request": request, 
            "facilities": facilities_list,
            "error": None
        })

    return templates.TemplateResponse("html.html", {
        "request": request, 
        "facilities": None,
        "error": "Category not found."
    })

print('test point3')

