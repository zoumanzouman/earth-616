from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Middleware for CORS
origins = ["http://127.0.0.1:8000/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Template setup
templates = Jinja2Templates(directory="frontend")

# Endpoint for homepage
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request): 
    return templates.TemplateResponse("html.html", {"request": request})

# Data
facilities_data = {
    "restaurants": [
        {"name": "Swarnamukhi", "location": "SriCity Center", "contact": "123-456-789", "hours": "10 AM - 9 PM"},
        {"name": "Quick Bites", "location": "SriCity Mall", "contact": "987-654-321", "hours": "11 AM - 10 PM"}
    ],
    "shops": [
        {"name": "The Fashion Store", "location": "SriCity Mall", "contact": "555-111-222", "hours": "10 AM - 8 PM"},
        {"name": "TechMart", "location": "Tech Plaza", "contact": "444-333-222", "hours": "9 AM - 7 PM"}
    ],
    "travel": [
        {"name": "SriCity Cab Service", "location": "SriCity Center", "contact": "111-222-333", "hours": "24/7"},
        {"name": "Local Bus Service", "location": "SriCity Bus Depot", "contact": "999-888-777", "hours": "6 AM - 11 PM"}
    ],
    "places_to_visit": [
        {"name": "Nature Park", "location": "North SriCity", "contact": "777-888-999", "hours": "6 AM - 6 PM"},
        {"name": "Historical Museum", "location": "SriCity Center", "contact": "444-555-666", "hours": "10 AM - 5 PM"}
    ],
    "hospitals": [
        {"name": "SriCity General Hospital", "location": "Main Road", "contact": "333-444-555", "hours": "24/7"},
        {"name": "SriCity Clinic", "location": "Tech Park", "contact": "222-111-999", "hours": "9 AM - 8 PM"}
    ]
}

# Endpoint for searching facilities
@app.get("/search", response_class=HTMLResponse)
async def search_facilities(request: Request, query: str):
    results = []
    for category, facilities in facilities_data.items():
        for facility in facilities:
            if query.lower() in facility["name"].lower():
                results.append(facility)
    return templates.TemplateResponse("html.html", {"request": request, "facilities": results if results else None, "error": "No facilities found." if not results else None})

# Endpoint for fetching facilities by category
@app.get("/{category}", response_class=HTMLResponse)
async def get_facilities(request: Request, category: str):
    if category in facilities_data:
        return templates.TemplateResponse("html.html", {"request": request, "facilities": facilities_data[category]})
    return templates.TemplateResponse("html.html", {"request": request, "error": "Category not found."})


