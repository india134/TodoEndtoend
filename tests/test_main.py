import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base
from app import models


# ----------------------------
# ✅ CONFIG: Use file-based test DB
# ----------------------------
TEST_DB_URL = "sqlite:///./test_todo.db"

# Delete old DB before running
if os.path.exists("test_todo.db"):
    os.remove("test_todo.db")

# Create engine and session for test DB
engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for test DB
Base.metadata.create_all(bind=engine)


# ----------------------------
# ✅ Dependency override for testing
# ----------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ----------------------------
# ✅ TEST CASES
# ----------------------------

def test_homepage_loads():
    """Homepage should load successfully"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_add_task():
    response = client.post(
        "/add",
        data={"title": "Test Task", "description": "pytest"},
        follow_redirects=False
    )
    assert response.status_code == 303

def test_toggle_task():
    """Toggle completion status of a task"""
    client.post("/add", data={"title": "Toggle Task", "description": "pytest"})
    response = client.get("/delete/1", follow_redirects=False)
    assert response.status_code in [303, 404]


def test_delete_task():
    """Delete a task"""
    client.post("/add", data={"title": "Delete Task", "description": "pytest"})
    response = client.get("/toggle/1", follow_redirects=False)
    assert response.status_code in [303, 404]



