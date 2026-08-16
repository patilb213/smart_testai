from flask import Blueprint, request, jsonify
from models.models import db, TestCase, TestStep
from utils.audit import write_audit_log
from auth.decorators import token_required

testcase_bp = Blueprint("testcases", __name__)

@testcase_bp.route("", methods=["POST"])
@token_required
def create_testcase():
    data = request.get_json()
    tc = TestCase(
        name=data.get("name"),
        target_url=data.get("target_url"),
        description=data.get("description"),
        created_by=None,
        status="active",
        version=1,
    )
    db.session.add(tc)
    db.session.commit()

    write_audit_log(
        action="TEST_CASE_CREATED", user=request.user_email, entity_type="TestCase",
        entity_id=tc.id, after_state={"name": tc.name, "target_url": tc.target_url},
        ip_address=request.remote_addr
    )
    return jsonify({"message": "test case created", "test_case_id": tc.id}), 201


@testcase_bp.route("", methods=["GET"])
@token_required
def list_testcases():
    cases = TestCase.query.all()
    result = [{"id": c.id, "name": c.name, "target_url": c.target_url, "status": c.status} for c in cases]
    return jsonify(result), 200


@testcase_bp.route("/<int:testcase_id>/steps", methods=["POST"])
@token_required
def add_steps(testcase_id):
    data = request.get_json()
    steps = data.get("steps", [])
    created = []
    for s in steps:
        step = TestStep(
            test_case_id=testcase_id,
            step_order=s.get("step_order"),
            action_type=s.get("action_type"),
            candidate_locators=s.get("candidate_locators"),
            input_value=s.get("input_value"),
            page_url=s.get("page_url"),
        )
        db.session.add(step)
        created.append(step)
    db.session.commit()

    write_audit_log(
        action="TEST_STEPS_ADDED", user=request.user_email, entity_type="TestCase",
        entity_id=testcase_id, after_state={"steps_added": len(created)},
        ip_address=request.remote_addr
    )
    return jsonify({"message": f"{len(created)} steps added"}), 201


@testcase_bp.route("/<int:testcase_id>/steps", methods=["GET"])
@token_required
def get_steps(testcase_id):
    steps = TestStep.query.filter_by(test_case_id=testcase_id).order_by(TestStep.step_order).all()
    result = [
        {
            "id": s.id,
            "step_order": s.step_order,
            "action_type": s.action_type,
            "candidate_locators": s.candidate_locators,
            "input_value": s.input_value,
            "page_url": s.page_url,
        }
        for s in steps
    ]
    return jsonify(result), 200