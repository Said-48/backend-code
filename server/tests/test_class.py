import pytest
from app.models import db, Class, User
from app.utils.auth import generate_jwt

# -----------------------------
# Helper to generate auth headers
# -----------------------------
def get_auth_header(client, email, password):
    login = client.post("/auth/login", json={"email": email, "password": password})
    token = login.json["token"]
    return {"Authorization": f"Bearer {token}"}

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def admin_user(app):
    db.session.query(User).filter_by(role="Admin").delete()
    db.session.commit()

    admin = User(name="Admin User", email="admin@test.com", role="Admin")
    admin.set_password("adminpass")
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def seed_class(app):
    db.session.query(Class).delete()
    db.session.commit()

    cls = Class(name="Test Class", description="Test Description", track="Fullstack")
    db.session.add(cls)
    db.session.commit()
    return cls

# -----------------------------
# Tests
# -----------------------------
def test_create_class(client, admin_user):
    headers = get_auth_header(client, admin_user.email, "adminpass")
    payload = {"name": "New Class", "description": "New Description", "track": "Data Science"}
    res = client.post("/classes/", json=payload, headers=headers)
    assert res.status_code == 201
    assert res.json["class"]["name"] == "New Class"
    assert res.json["class"]["track"] == "Data Science"

def test_create_class_duplicate(client, admin_user, seed_class):
    headers = get_auth_header(client, admin_user.email, "adminpass")
    payload = {"name": seed_class.name, "description": "Duplicate", "track": "Fullstack"}
    res = client.post("/classes/", json=payload, headers=headers)
    assert res.status_code == 409

def test_get_classes(client, seed_class):
    res = client.get("/classes/")
    assert res.status_code == 200
    assert len(res.json) > 0

def test_get_single_class(client, seed_class):
    res = client.get(f"/classes/{seed_class.id}")
    assert res.status_code == 200
    assert res.json["id"] == seed_class.id

def test_update_class(client, admin_user, seed_class):
    headers = get_auth_header(client, admin_user.email, "adminpass")
    payload = {"name": "Updated Class", "track": "Android"}
    res = client.put(f"/classes/{seed_class.id}", json=payload, headers=headers)
    assert res.status_code == 200
    updated = db.session.get(Class, seed_class.id)
    assert updated.name == "Updated Class"
    assert updated.track == "Android"

def test_delete_class(client, admin_user, seed_class):
    headers = get_auth_header(client, admin_user.email, "adminpass")
    res = client.delete(f"/classes/{seed_class.id}", headers=headers)
    assert res.status_code == 200
    deleted = db.session.get(Class, seed_class.id)
    assert deleted is None
