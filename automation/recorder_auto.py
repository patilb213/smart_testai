import sys
import time
import json
import os
import requests
from playwright.sync_api import sync_playwright

API_BASE = "http://127.0.0.1:5000"


def record_session(target_url, record_seconds=60):
    captured_steps = []
    step_counter = {"count": 0}

    def handle_event(event_data):
        step_counter["count"] += 1
        event_data["step_order"] = step_counter["count"]
        event_data["timestamp"] = time.time()
        captured_steps.append(event_data)
        print(f"Captured step {step_counter['count']}: {event_data['action_type']}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.expose_function("recordEvent", handle_event)

        page.add_init_script("""
            function getLocators(el) {
                const locators = [];
                if (el.id) locators.push({strategy: "id", value: "#" + el.id});
                if (el.getAttribute("name")) locators.push({strategy: "name", value: el.getAttribute("name")});
                if (el.innerText && el.innerText.trim().length < 50) {
                    locators.push({strategy: "text", value: el.innerText.trim()});
                }
                let path = el.tagName.toLowerCase();
                if (el.className) path += "." + el.className.toString().split(" ").join(".");
                locators.push({strategy: "css", value: path});
                return locators;
            }
            document.addEventListener("click", (e) => {
                window.recordEvent({action_type: "click", candidate_locators: getLocators(e.target), page_url: window.location.href});
            }, true);
            let inputTimers = new WeakMap();
            document.addEventListener("input", (e) => {
                const el = e.target;
                if (inputTimers.has(el)) clearTimeout(inputTimers.get(el));
                const timer = setTimeout(() => {
                    window.recordEvent({action_type: "input", candidate_locators: getLocators(el), input_value: el.value, page_url: window.location.href});
                    inputTimers.delete(el);
                }, 600);
                inputTimers.set(el, timer);
            }, true);
            document.addEventListener("change", (e) => {
                if (e.target.tagName === "SELECT") {
                    window.recordEvent({action_type: "select", candidate_locators: getLocators(e.target), input_value: e.target.value, page_url: window.location.href});
                }
            }, true);
            document.addEventListener("submit", (e) => {
                window.recordEvent({action_type: "submit", candidate_locators: getLocators(e.target), page_url: window.location.href});
            }, true);
        """)

        page.goto(target_url)
        print(f"Recording... you have {record_seconds} seconds. Interact now.")
        time.sleep(record_seconds)
        browser.close()

    return captured_steps


def save_to_backend(auth_token, name, target_url, steps):
    headers = {"Authorization": f"Bearer {auth_token}"}
    tc_response = requests.post(f"{API_BASE}/testcases", headers=headers,
                                 json={"name": name, "target_url": target_url, "description": "Recorded via UI"})
    tc_response.raise_for_status()
    test_case_id = tc_response.json()["test_case_id"]

    steps_response = requests.post(f"{API_BASE}/testcases/{test_case_id}/steps", headers=headers, json={"steps": steps})
    steps_response.raise_for_status()
    print(f"Saved test case {test_case_id} with {len(steps)} steps")
    return test_case_id


if __name__ == "__main__":
    target_url = sys.argv[1]
    name = sys.argv[2]
    token = sys.argv[3]

    steps = record_session(target_url, record_seconds=60)
    print(f"Captured {len(steps)} steps total")

    if steps:
        save_to_backend(token, name, target_url, steps)
    else:
        print("No steps captured — nothing saved")