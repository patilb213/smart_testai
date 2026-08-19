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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class TestCase(db.Model):
    __tablename__ = "test_cases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    target_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="active")
    version = db.Column(db.Integer, default=1)

    steps = db.relationship(
        "TestStep", backref="test_case", cascade="all, delete-orphan", lazy="joined"
    )
    runs = db.relationship(
        "TestRun", backref="test_case", cascade="all, delete-orphan", lazy="dynamic"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "target_url": self.target_url,
            "description": self.description,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status,
            "version": self.version,
            "steps_count": len(self.steps) if self.steps else 0,
        }


class TestStep(db.Model):
    __tablename__ = "test_steps"

    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(
        db.Integer, db.ForeignKey("test_cases.id"), nullable=False
    )
    step_order = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    candidate_locators = db.Column(db.JSON, nullable=True)
    input_value = db.Column(db.String(255), nullable=True)
    page_url = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "test_case_id": self.test_case_id,
            "step_order": self.step_order,
            "action_type": self.action_type,
            "description": self.description,
            "candidate_locators": self.candidate_locators or [],
            "input_value": self.input_value,
            "page_url": self.page_url,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


class TestRun(db.Model):
    __tablename__ = "test_runs"

    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(
        db.Integer, db.ForeignKey("test_cases.id"), nullable=False
    )
    status = db.Column(
        db.String(50), default="running"
    )  # running, passed, self_healed, failed, error
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    duration_ms = db.Column(db.Integer, default=0)
    triggered_by = db.Column(db.String(150), default="test@example.com")
    error_message = db.Column(db.Text, nullable=True)
    steps_total = db.Column(db.Integer, default=0)
    steps_passed = db.Column(db.Integer, default=0)
    steps_healed = db.Column(db.Integer, default=0)
    steps_failed = db.Column(db.Integer, default=0)
    logs = db.Column(db.Text, default="")

    run_steps = db.relationship(
        "TestRunStep", backref="test_run", cascade="all, delete-orphan", lazy="joined"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "run_number": self.id,
            "test_case_id": self.test_case_id,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "executed_at": (
                self.completed_at.strftime("%m/%d/%Y, %I:%M:%S %p")
                if self.completed_at
                else (
                    self.started_at.strftime("%m/%d/%Y, %I:%M:%S %p")
                    if self.started_at
                    else "N/A"
                )
            ),
            "duration_ms": self.duration_ms or 0,
            "triggered_by": self.triggered_by or "test@example.com",
            "error_message": self.error_message,
            "steps_total": self.steps_total or len(self.run_steps),
            "steps_passed": self.steps_passed or 0,
            "steps_healed": self.steps_healed or 0,
            "steps_failed": self.steps_failed or 0,
            "logs": self.logs.split("\n") if self.logs else [],
        }


class TestRunStep(db.Model):
    __tablename__ = "test_run_steps"

    id = db.Column(db.Integer, primary_key=True)
    test_run_id = db.Column(
        db.Integer, db.ForeignKey("test_runs.id"), nullable=False
    )
    test_step_id = db.Column(
        db.Integer, db.ForeignKey("test_steps.id"), nullable=True
    )
    step_order = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.String(50), nullable=False, default="passed"
    )  # passed, self_healed, failed, skipped
    resolved_locator_strategy = db.Column(db.String(50), nullable=True)
    resolved_locator_value = db.Column(db.String(255), nullable=True)
    confidence = db.Column(db.Float, default=1.0)
    healing_metadata = db.Column(db.JSON, nullable=True)
    execution_time_ms = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "test_run_id": self.test_run_id,
            "test_step_id": self.test_step_id,
            "step_order": self.step_order,
            "action_type": self.action_type,
            "description": self.description,
            "status": self.status,
            "resolved_locator_strategy": self.resolved_locator_strategy,
            "resolved_locator_value": self.resolved_locator_value,
            "confidence": self.confidence,
            "healing_metadata": self.healing_metadata,
            "execution_time_ms": self.execution_time_ms,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action,
            "user": self.user,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


class ChangeEvent(db.Model):
    __tablename__ = "change_events"

    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(
        db.Integer, db.ForeignKey("test_cases.id"), nullable=False
    )
    run_id = db.Column(db.Integer, db.ForeignKey("test_runs.id"), nullable=False)
    previous_run_id = db.Column(db.Integer, nullable=True)
    change_type = db.Column(
        db.String(50)
    )  # SELF_HEALED, NEW_FAILURE, RECOVERED
    step_order = db.Column(db.Integer)
    description = db.Column(db.String(255))
    severity = db.Column(db.String(20), default="medium")
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "test_case_id": self.test_case_id,
            "run_id": self.run_id,
            "previous_run_id": self.previous_run_id,
            "change_type": self.change_type,
            "step_order": self.step_order,
            "description": self.description,
            "severity": self.severity,
            "detected_at": (
                self.detected_at.isoformat() if self.detected_at else None
            ),
        }