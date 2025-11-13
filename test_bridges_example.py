"""
Example test file for Bridges router
Use this as a reference for testing your own routers

To run tests:
1. Install pytest: pip install pytest httpx
2. Run: pytest test_bridges_example.py -v
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_bridge_helper(full_result=False):
    """Helper to create a new bridge"""
    response = client.post(
        "/api/bridges/",
        json={
            "name": "Test Bridge",
            "location": "Test City",
            "length_meters": 500.0,
            "width_meters": 20.0,
            "max_load_rating_tons": 50.0,
            "condition": "good",
            "year_built": "2020",
            "material": "concrete"
        }
    )
    if full_result:
        return response
    else:
        data = response.json()
        return data["id"]

def test_create_bridge():
    """Test creating a new bridge"""
    response = create_bridge_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Bridge"
    assert data["location"] == "Test City"
    assert "id" in data

def test_list_bridges():
    """Test listing all bridges"""
    response = client.get("/api/bridges/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "bridges" in data
    assert isinstance(data["bridges"], list)


def test_get_bridge():
    """Test getting a specific bridge"""
    # First create a bridge
    bridge_id = create_bridge_helper()

    # Then retrieve it
    response = client.get(f"/api/bridges/{bridge_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == bridge_id


def test_update_bridge():
    """Test updating a bridge"""
    # First create a bridge
    bridge_id = create_bridge_helper()

    # Then update it
    response = client.put(
        f"/api/bridges/{bridge_id}",
        json={"condition": "fair"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["condition"] == "fair"


def test_delete_bridge():
    """Test deleting a bridge"""
    # First create a bridge
    bridge_id = create_bridge_helper()

    # Then delete it
    response = client.delete(f"/api/bridges/{bridge_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/bridges/{bridge_id}")
    assert response.status_code == 404


def test_get_nonexistent_bridge():
    """Test getting a bridge that doesn't exist"""
    response = client.get("/api/bridges/99999")
    assert response.status_code == 404


def test_filter_by_condition():
    """Test filtering bridges by condition"""
    response = client.get("/api/bridges/?condition=good")
    assert response.status_code == 200


def test_search_bridges():
    """Test searching bridges"""
    response = client.get("/api/bridges/?search=Test")
    assert response.status_code == 200


if __name__ == "__main__":
    print("Run with: pytest test_bridges_example.py -v")
