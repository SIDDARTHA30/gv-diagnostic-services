from .conftest import client


def test_valid_booking():
    response = client.post(
        "/api/bookings",
        json={"name": "Test Patient", "phone": "9866020079", "test": "CBC", "collection_type": "Centre Visit"},
    )
    assert response.status_code == 201
    assert response.json()["reference_number"].startswith("GV-")


def test_missing_booking_fields():
    response = client.post("/api/bookings", json={"phone": "9866020079"})
    assert response.status_code == 422


def test_home_pickup_requires_address():
    response = client.post(
        "/api/bookings",
        json={"name": "Test Patient", "phone": "9866020079", "test": "CBC", "collection_type": "Home Sample Pickup"},
    )
    assert response.status_code == 422


def test_valid_contact():
    response = client.post(
        "/api/contact",
        json={
            "name": "Test Patient",
            "phone": "9866020079",
            "email": "patient@example.com",
            "subject": "Question",
            "message": "Please call me.",
        },
    )
    assert response.status_code == 201
    assert response.json()["reference_number"].startswith("GV-")


def test_invalid_contact_email():
    response = client.post(
        "/api/contact",
        json={"name": "Test Patient", "phone": "9866020079", "email": "not-an-email", "subject": "Question", "message": "Hello"},
    )
    assert response.status_code == 422
