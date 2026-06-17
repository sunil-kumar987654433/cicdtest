import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import app
from src.db.database import get_session

client = TestClient(app)

# 1. Database connection mocking wrapper utility for standalone execution
async def override_get_session():
    # Database calls mimic karne ke liye empty iterator pass-through handle kiya
    yield None

# App configuration dependency injection overwrite runtime
app.dependency_overrides[get_session] = override_get_session

def test_health_check(mocker):
    """
    Test for the /health endpoint with database dependency mocked.
    """
    # SQLAlchemy execution flow bypass layer for unit testing safety
    mocker.patch.object(AsyncSession, 'execute', return_value=None)
    
    response = client.get("/health")
    assert response.status_code == 200
    # FIX: Sahi response assertion logic map kiya
    assert response.json() == "connected"


def test_root_returns_json():
    """
    Test for root URL format validation mapping logic.
    """
    r = client.get("/")
    assert r.status_code == 200
    # FIX: Expected response structure JSON match implementation
    assert "application/json" in r.headers['content-type']
    assert r.json()["status"] == "healthy"
