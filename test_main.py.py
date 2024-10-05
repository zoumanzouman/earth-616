import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db  # Import your FastAPI app and DB dependency
from database import Base

# Test client for FastAPI
client = TestClient(app)

# Set up an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing DB
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = test_db

### Test Cases



# Test search facilities
def test_search_facilities(test_db):
    # Assuming there is test data added in test_db
    response = client.get("/search?query=test_facility")
    assert response.status_code == 200
    assert "test_facility" in response.text

# Test admin login page
def test_get_admin_login():
    response = client.get("/admin_login")
    assert response.status_code == 200
    assert "Admin Login" in response.text  # Update with actual content

# Test fetching facilities by category
@pytest.mark.parametrize("category", ["restaurants", "shops", "hospitals", "places_to_visit"])
def test_get_facilities_by_category(category, test_db):
    response = client.get(f"/{category}")
    assert response.status_code == 200
    assert category in response.text

# Test token generation (login)
def test_login_for_access_token(test_db):
    # Create a test user
    user_data = {"username": "test_user", "password": "test_pass"}
    response = client.post("/token", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test admin-only route
def test_admin_route(test_db):
    # Assuming there's a test admin user created
    admin_token = "admin_token_here"  # Replace with a valid token during testing
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/admin/", headers=headers)
    assert response.status_code == 200
    assert "admin" in response.text
