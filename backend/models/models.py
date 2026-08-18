from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="tester")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TestCase(db.Model):
    __tablename__ = "test_cases"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    target_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="active")
    version = db.Column(db.Integer, default=1)

    steps = db.relationship("TestStep", backref="test_case", cascade="all, delete-orphan")


class TestStep(db.Model):
    __tablename__ = "test_steps"
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_cases.id"), nullable=False)
    step_order = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    candidate_locators = db.Column(db.JSON)
    input_value = db.Column(db.String(255))
    page_url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class AuditLog(db.Model):
    __tablename__ = "audit_log"
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(150))
    entity_type = db.Column(db.String(100))
    entity_id = db.Column(db.Integer)
    before_state = db.Column(db.JSON)
    after_state = db.Column(db.JSON)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    previous_hash = db.Column(db.String(64))
    hash = db.Column(db.String(64))