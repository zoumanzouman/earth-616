from models import User, UserRole
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
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


# Template setup
templates = Jinja2Templates(directory="frontend")

# Mounting the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.get("/admin_login", response_class=HTMLResponse)
async def get_admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def get_admin_dashboard(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

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



# Authentication and Authorization
SECRET_KEY = "your-secret-key"  # In production, use a secure method to generate and store this
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

# Authorization decorator
def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

# Token endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Example protected route
@app.get("/users/me/", response_model=dict)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return {"username": current_user.username, "role": current_user.role.value}

# Example admin-only route
@app.get("/admin/")
async def admin_route(current_user: User = Depends(admin_required)):
    return {"message": "This is an admin-only route", "admin": current_user.username}

# Function to add a user to the database
def add_user(db: Session, username: str, password: str, role: models.UserRole):
    hashed_password = get_password_hash(password)
    db_user = models.User(username=username, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Example usage:
# with SessionLocal() as db:
#     add_user(db, "student1", "password123", models.UserRole.student)
#     add_user(db, "admin1", "adminpass", UserRole.admin)


def run_app():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


def add_data(db: Session, data: dict):
    pass
def remove_data(db: Session, data_id: int):
    pass
def edit_data(db: Session, data_id: int, new_data: dict):
    pass
    


