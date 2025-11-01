# tests/conftest.py
import os
import pytest
from unittest.mock import patch
from run import create_app
from app.models import db, User

# -----------------------------
# App fixture
# -----------------------------
@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:newpassword@localhost:5432/projectx_db"
        ),
        "SECRET_KEY": "testsecretkey",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()  # Ensure tables exist
        yield app
        db.session.remove()
        db.drop_all()  # Clean up after tests

# -----------------------------
# Client fixture
# -----------------------------
@pytest.fixture
def client(app):
    """Provide a Flask test client."""
    return app.test_client()

# -----------------------------
# Optional: Mock email sending (if function exists)
# -----------------------------
@pytest.fixture(autouse=True)
def mock_email():
    """
    Patch send_verification_email if it exists.
    Safe to run even if the function was removed.
    """
    try:
        from app.routes import auth_routes
        if hasattr(auth_routes, "send_verification_email"):
            send_patch = patch("app.routes.auth_routes.send_verification_email")
            mock_send = send_patch.start()
            mock_send.return_value = True
            yield mock_send
            send_patch.stop()
        else:
            yield None
    except ImportError:
        yield None

# -----------------------------
# Ensure admin exists
# -----------------------------
@pytest.fixture(autouse=True)
def ensure_admin_exists(app):
    """Ensure an admin user exists in the test DB."""
    with app.app_context():
        admin = User.query.filter_by(email="admin@test.com").first()
        if not admin:
            admin = User(
                name="Admin User",
                email="admin@test.com",
                role="Admin"
            )
            admin.set_password(os.environ.get("ADMIN_PASSWORD", "adminpass"))
            db.session.add(admin)
            db.session.commit()

# -----------------------------
# Seed a test student
# -----------------------------
@pytest.fixture(autouse=True)
def seed_test_users(app):
    """Ensure at least one test student exists in the test DB."""
    with app.app_context():
        student = User.query.filter_by(email="student1@example.com").first()
        if not student:
            student = User(
                name="Student 1",
                email="student1@example.com",
                role="Student"
            )
            student.set_password(os.environ.get("STUDENT_PASSWORD", "studentpass"))
            db.session.add(student)
            db.session.commit()

# -----------------------------
# Optional: Seed additional test users
# -----------------------------
@pytest.fixture(autouse=True)
def seed_additional_students(app):
    """Seed multiple test students for more comprehensive tests."""
    with app.app_context():
        test_users = [
            {"name": "Student 2", "email": "student2@example.com"},
            {"name": "Student 3", "email": "student3@example.com"},
        ]
        for u in test_users:
            if not User.query.filter_by(email=u["email"]).first():
                user = User(
                    name=u["name"],
                    email=u["email"],
                    role="Student"
                )
                user.set_password(os.environ.get("STUDENT_PASSWORD", "studentpass"))
                db.session.add(user)
        db.session.commit()
