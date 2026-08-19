from flask import Blueprint, request, jsonify
from datetime import datetime
import subprocess
import threading
import sys
import os

from models.models import (
    db,
    TestCase,
    TestStep,
    TestRun,
    TestRunStep,
    ChangeEvent,
)

from utils.audit import write_audit_log
from auth.decorators import token_required


execution_bp = Blueprint("executions", __name__)


def execute_runner_process(target_url, test_case_id, run_id, token):
    """
    Spawns the Playwright runner process in the background.
    """
    try:
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        script_path = os.path.join(
            project_root,
            "automation",
            "runner_auto.py",
        )

        process = subprocess.Popen(
            [
                sys.executable,
                "-u",
                script_path,
                str(test_case_id),
                str(run_id),
                token,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        for line in process.stdout:
            print(f"[RUNNER #{run_id}] {line.strip()}")

        process.wait(timeout=180)

    except subprocess.TimeoutExpired:
        print(f"[RUNNER TIMEOUT #{run_id}] Process exceeded timeout limit.")
        with db.app.app_context():
            run = TestRun.query.get(run_id)
            if run and run.status == "running":
                run.status = "failed"
                run.error_message = "Execution timed out after 180 seconds"
                run.completed_at = datetime.utcnow()
                db.session.commit()

    except Exception as e:
        print(f"[RUNNER ERROR #{run_id}] {str(e)}")
        with db.app.app_context():
            run = TestRun.query.get(run_id)
            if run and run.status == "running":
                run.status = "failed"
                run.error_message = f"Process launch error: {str(e)}"
                run.completed_at = datetime.utcnow()
                db.session.commit()


@execution_bp.route("/start", methods=["POST"])
@token_required
def start_execution():
    data = request.get_json() or {}
    test_case_id = data.get("test_case_id")

    if not test_case_id:
        return jsonify({"error": "test_case_id is required"}), 400

    test_case = TestCase.query.get(test_case_id)

    if not test_case:
        return jsonify({"error": "Test case not found"}), 404

    steps_count = TestStep.query.filter_by(
        test_case_id=test_case_id
    ).count()

    user_email = getattr(request, "user_email", "test@example.com")

    run = TestRun(
        test_case_id=test_case_id,
        status="running",
        started_at=datetime.utcnow(),
        triggered_by=user_email,
        steps_total=steps_count,
        steps_passed=0,
        steps_failed=0,
    )

    db.session.add(run)
    db.session.commit()

    write_audit_log(
        action="TEST_RUN_STARTED",
        user=user_email,
        entity_type="TestRun",
        entity_id=run.id,
        after_state={
            "test_case_id": test_case_id,
            "status": "running",
        },
        ip_address=request.remote_addr,
    )

    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header

    thread = threading.Thread(
        target=execute_runner_process,
        args=(
            test_case.target_url,
            test_case_id,
            run.id,
            token,
        ),
    )

    thread.daemon = True
    thread.start()

    return jsonify(
        {
            "message": "Regression test run started",
            "run_id": run.id,
            "test_case_id": test_case_id,
            "status": "running",
            "executed_at": run.started_at.strftime("%m/%d/%Y, %I:%M:%S %p"),
        }
    ), 202


@execution_bp.route("/<int:run_id>/step", methods=["POST"])
@token_required
def record_step_result(run_id):
    data = request.get_json() or {}

    run = TestRun.query.get(run_id)

    if not run:
        return jsonify({"error": "Test run not found"}), 404

    step_status = data.get("status", "passed")

    step_result = TestRunStep(
        test_run_id=run_id,
        test_step_id=data.get("test_step_id"),
        step_order=data.get("step_order", 0),
        action_type=data.get("action_type", "unknown"),
        description=data.get("description"),
        status=step_status,
        resolved_locator_strategy=data.get("resolved_locator_strategy"),
        resolved_locator_value=data.get("resolved_locator_value"),
        execution_time_ms=data.get("execution_time_ms", 0),
        error_message=data.get("error_message"),
        timestamp=datetime.utcnow(),
    )

    db.session.add(step_result)

    # Count both 'passed' and 'self_healed' steps as successful executions
    if step_status in ("passed", "self_healed"):
        run.steps_passed = (run.steps_passed or 0) + 1
    else:
        run.steps_failed = (run.steps_failed or 0) + 1

    db.session.commit()

    return jsonify({"message": "Step recorded", "status": step_status}), 201


def detect_changes(run_id):
    """
    Compares current run with previous run to detect NEW_FAILURE, RECOVERED,
    or SELF_HEALED drift events.
    """
    run = TestRun.query.get(run_id)

    if not run:
        return

    previous_run = (
        TestRun.query.filter(
            TestRun.test_case_id == run.test_case_id,
            TestRun.id < run.id,
            TestRun.status.in_(["passed", "self_healed", "failed"]),
        )
        .order_by(TestRun.id.desc())
        .first()
    )

    current_steps = {
        s.step_order: s
        for s in TestRunStep.query.filter_by(test_run_id=run.id).all()
    }

    # If this is the baseline run, also check for any step marked 'self_healed'
    for order, cur in current_steps.items():
        if cur.status == "self_healed":
            event = ChangeEvent(
                test_case_id=run.test_case_id,
                run_id=run.id,
                previous_run_id=previous_run.id if previous_run else run.id,
                change_type="SELF_HEALED",
                step_order=order,
                description=(
                    f"Step {order} ({cur.description or cur.action_type}) "
                    f"drifted and autonomously recovered via locator: "
                    f"'{cur.resolved_locator_value}' ({cur.resolved_locator_strategy})"
                ),
                severity="medium",
            )
            db.session.add(event)

    if not previous_run:
        db.session.commit()
        return

    previous_steps = {
        s.step_order: s
        for s in TestRunStep.query.filter_by(test_run_id=previous_run.id).all()
    }

    for order, cur in current_steps.items():
        prev = previous_steps.get(order)

        if not prev:
            continue

        event = None

        if prev.status in ("passed", "self_healed") and cur.status == "failed":
            event = ChangeEvent(
                test_case_id=run.test_case_id,
                run_id=run.id,
                previous_run_id=previous_run.id,
                change_type="NEW_FAILURE",
                step_order=order,
                description=(
                    f"Step {order} ({cur.description or cur.action_type}) "
                    f"started failing: {cur.error_message}"
                ),
                severity="high",
            )

        elif prev.status == "failed" and cur.status in ("passed", "self_healed"):
            event = ChangeEvent(
                test_case_id=run.test_case_id,
                run_id=run.id,
                previous_run_id=previous_run.id,
                change_type="RECOVERED",
                step_order=order,
                description=(
                    f"Step {order} ({cur.description or cur.action_type}) "
                    f"recovered and now passes"
                ),
                severity="low",
            )

        elif (
            prev.resolved_locator_strategy
            and cur.resolved_locator_strategy
            and (prev.resolved_locator_strategy != cur.resolved_locator_strategy)
            and cur.status != "self_healed"  # avoid double adding
        ):
            event = ChangeEvent(
                test_case_id=run.test_case_id,
                run_id=run.id,
                previous_run_id=previous_run.id,
                change_type="SELF_HEALED",
                step_order=order,
                description=(
                    f"Step {order} ({cur.description or cur.action_type}) "
                    f"locator drifted from '{prev.resolved_locator_strategy}' "
                    f"to '{cur.resolved_locator_strategy}' — self-healing engaged"
                ),
                severity="medium",
            )

        if event:
            db.session.add(event)

    db.session.commit()


@execution_bp.route("/<int:run_id>/complete", methods=["POST"])
@token_required
def complete_run(run_id):
    data = request.get_json() or {}

    run = TestRun.query.get(run_id)

    if not run:
        return jsonify({"error": "Test run not found"}), 404

    run.status = data.get("status", "passed")
    run.completed_at = datetime.utcnow()
    run.duration_ms = data.get("duration_ms", 0)
    run.error_message = data.get("error_message")

    if "steps_passed" in data:
        run.steps_passed = data.get("steps_passed")

    if "steps_failed" in data:
        run.steps_failed = data.get("steps_failed")

    db.session.commit()
    detect_changes(run_id)

    user_email = getattr(request, "user_email", "test@example.com")
    write_audit_log(
        action="TEST_RUN_COMPLETED",
        user=user_email,
        entity_type="TestRun",
        entity_id=run.id,
        after_state={
            "status": run.status,
            "duration_ms": run.duration_ms,
            "passed": run.steps_passed,
            "failed": run.steps_failed,
        },
        ip_address=request.remote_addr,
    )

    return jsonify(
        {
            "message": "Test run marked complete",
            "status": run.status,
            "duration_ms": run.duration_ms,
            "steps_passed": run.steps_passed,
            "steps_total": run.steps_total,
        }
    ), 200


@execution_bp.route("/testcase/<int:test_case_id>", methods=["GET"])
@token_required
def get_runs_for_testcase(test_case_id):
    runs = (
        TestRun.query.filter_by(test_case_id=test_case_id)
        .order_by(TestRun.id.desc())
        .all()
    )

    results = [
        {
            "id": r.id,
            "run_number": r.id,
            "test_case_id": r.test_case_id,
            "status": r.status,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "executed_at": (
                r.completed_at.strftime("%m/%d/%Y, %I:%M:%S %p")
                if r.completed_at
                else (
                    r.started_at.strftime("%m/%d/%Y, %I:%M:%S %p")
                    if r.started_at
                    else "N/A"
                )
            ),
            "duration_ms": r.duration_ms or 0,
            "triggered_by": r.triggered_by or "test@example.com",
            "error_message": r.error_message,
            "steps_total": r.steps_total or 4,
            "steps_passed": r.steps_passed or 0,
            "steps_failed": r.steps_failed or 0,
        }
        for r in runs
    ]

    return jsonify(results), 200


@execution_bp.route("/<int:run_id>", methods=["GET"])
@token_required
def get_run_detail(run_id):
    run = TestRun.query.get(run_id)

    if not run:
        return jsonify({"error": "Run not found"}), 404

    steps = (
        TestRunStep.query.filter_by(test_run_id=run_id)
        .order_by(TestRunStep.step_order)
        .all()
    )

    steps_data = [
        {
            "id": s.id,
            "step_order": s.step_order,
            "action_type": s.action_type,
            "description": s.description,
            "status": s.status,
            "resolved_locator_strategy": s.resolved_locator_strategy,
            "resolved_locator_value": s.resolved_locator_value,
            "execution_time_ms": s.execution_time_ms,
            "error_message": s.error_message,
            "timestamp": s.timestamp.isoformat() if s.timestamp else None,
        }
        for s in steps
    ]

    return jsonify(
        {
            "id": run.id,
            "run_number": run.id,
            "test_case_id": run.test_case_id,
            "status": run.status,
            "started_at": run.started_at.isoformat() if run.started_at else None,
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
            "executed_at": (
                run.completed_at.strftime("%m/%d/%Y, %I:%M:%S %p")
                if run.completed_at
                else (
                    run.started_at.strftime("%m/%d/%Y, %I:%M:%S %p")
                    if run.started_at
                    else "N/A"
                )
            ),
            "duration_ms": run.duration_ms or 0,
            "triggered_by": run.triggered_by or "test@example.com",
            "error_message": run.error_message,
            "steps_total": run.steps_total or len(steps_data),
            "steps_passed": run.steps_passed or 0,
            "steps_failed": run.steps_failed or 0,
            "steps": steps_data,
        }
    ), 200


@execution_bp.route("/testcase/<int:test_case_id>/changes", methods=["GET"])
@token_required
def get_changes(test_case_id):
    events = (
        ChangeEvent.query.filter_by(test_case_id=test_case_id)
        .order_by(ChangeEvent.id.desc())
        .all()
    )

    result = [
        {
            "id": e.id,
            "run_id": e.run_id,
            "previous_run_id": e.previous_run_id,
            "change_type": e.change_type,
            "step_order": e.step_order,
            "description": e.description,
            "severity": e.severity,
            "detected_at": e.detected_at.isoformat() if e.detected_at else None,
        }
        for e in events
    ]

    return jsonify(result), 200