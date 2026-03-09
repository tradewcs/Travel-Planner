import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app

client = TestClient(app)


def test_create_project():
    response = client.post(
        "/api/v1/projects/",
        json={
            "name": "Paris Trip",
            "description": "Visit museums",
            "start_date": "2026-06-01",
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Paris Trip"
    assert data["description"] == "Visit museums"
    assert data["status"] == "active"
    assert "id" in data


def test_list_projects():
    response = client.get("/api/v1/projects/")

    assert response.status_code == 200
    assert "items" in response.json()
    assert "total" in response.json()


def test_get_project_not_found():
    fake_id = str(uuid4())
    response = client.get(f"/api/v1/projects/{fake_id}")

    assert response.status_code == 404
