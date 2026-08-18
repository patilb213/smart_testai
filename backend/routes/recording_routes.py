from flask import Blueprint, request, jsonify
import subprocess
import threading
import sys
import os
from auth.decorators import token_required

recording_bp = Blueprint("recording", __name__)

recording_status = {
    "running": False,
    "log": [],
    "error": None,
}


def run_recorder_process(target_url, name, token):
    recording_status["running"] = True
    recording_status["log"] = []
    recording_status["error"] = None

    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        script_path = os.path.join(project_root, "automation", "recorder_auto.py")

        process = subprocess.Popen(
            [sys.executable, "-u", script_path, target_url, name, token],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        for line in process.stdout:
            line = line.strip()
            if line:
                recording_status["log"].append(line)

        process.wait(timeout=120)

        if process.returncode != 0:
            recording_status["error"] = f"Recorder process failed (exit code {process.returncode})"

    except Exception as e:
        recording_status["error"] = str(e)
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

    if not target_url or not name:
        return jsonify({"error": "target_url and name are required"}), 400

    token = request.headers.get("Authorization").split(" ")[1]

    thread = threading.Thread(target=run_recorder_process, args=(target_url, name, token))
    thread.start()

    return jsonify({"message": "Recording started"}), 202


@recording_bp.route("/status", methods=["GET"])
@token_required
def recording_status_check():
    return jsonify(recording_status), 200