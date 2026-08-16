from flask import Blueprint, request, jsonify
import subprocess
import threading
import os
from auth.decorators import token_required

recording_bp = Blueprint("recording", __name__)

recording_status = {"running": False, "last_result": None}


def run_recorder_process(target_url, name, token):
    recording_status["running"] = True
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        script_path = os.path.join(project_root, "automation", "recorder_auto.py")

        result = subprocess.run(
            ["python", script_path, target_url, name, token],
            capture_output=True, text=True, timeout=300
        )
        recording_status["last_result"] = result.stdout + result.stderr
    except Exception as e:
        recording_status["last_result"] = str(e)
    finally:
        recording_status["running"] = False


@recording_bp.route("/start", methods=["POST"])
@token_required
def start_recording():
    if recording_status["running"]:
        return jsonify({"error": "A recording is already in progress"}), 409

    data = request.get_json()
    target_url = data.get("target_url")
    name = data.get("name")

    token = request.headers.get("Authorization").split(" ")[1]

    thread = threading.Thread(target=run_recorder_process, args=(target_url, name, token))
    thread.start()

    return jsonify({"message": "Recording started. Interact with the browser window that opens."}), 202


@recording_bp.route("/status", methods=["GET"])
@token_required
def recording_status_check():
    return jsonify(recording_status), 200