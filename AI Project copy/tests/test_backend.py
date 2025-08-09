import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.models import Post, Profile

# Create a test client
client = TestClient(app)

# Setup and teardown for tests
@pytest.fixture(scope="function")
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend is running!"}

def test_generate_content():
    """Test content generation endpoint."""
    response = client.post("/content/generate", json={"prompt": "AI trends in 2025"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "post" in data
    assert "content" in data["post"]

def test_list_posts():
    """Test listing posts."""
    response = client.get("/content/list")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "posts" in data

def test_create_profile():
    """Test profile creation."""
    response = client.post("/profile/", params={
        "name": "Test User",
        "headline": "AI Developer",
        "about": "Testing the LinkedIn AI agent"
    })
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "profile" in data

def test_get_profile():
    """Test getting profile."""
    # First create a profile
    client.post("/profile/", params={
        "name": "Test User",
        "headline": "AI Developer",
        "about": "Testing the LinkedIn AI agent"
    })
    
    # Then get it
    response = client.get("/profile/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data

def test_get_trends():
    """Test getting trends."""
    response = client.get("/trends/")
    assert response.status_code == 200
    data = response.json()
    assert "trends" in data
    assert "count" in data

def test_get_analytics():
    """Test getting analytics."""
    response = client.get("/analytics/")
    assert response.status_code == 200
    data = response.json()
    assert "total_posts" in data or "message" in data

def test_schedule_post():
    """Test scheduling a post."""
    # First create a post
    response = client.post("/content/generate", json={"prompt": "Test post for scheduling"})
    assert response.status_code == 200
    post_data = response.json()
    post_id = post_data["post"]["id"]
    
    # Then schedule it
    response = client.post("/content/schedule", params={
        "post_id": post_id,
        "delay_minutes": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "post_id" in data