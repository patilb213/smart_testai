import sys
import time
import json
import requests
from playwright.sync_api import sync_playwright

API_BASE = "http://127.0.0.1:5000"


def try_locator(page, locator):
    strategy = locator.get("strategy")
    value = locator.get("value")
    try:
        if strategy == "text":
            el = page.get_by_text(value, exact=False)
        else:
            el = page.locator(value) if strategy in ("id", "css") else page.locator(f'[name="{value}"]')
        if el.count() > 0:
            return el.first
    except Exception:
        return None
    return None


def execute_step(page, step):
    locators = step.get("candidate_locators") or []
    action_type = step.get("action_type")
    input_value = step.get("input_value")

    if action_type == "navigate":
        return {"status": "passed", "locator_used": None, "error": None}

    used_locator = None
    element = None
    healed = False

    for i, loc in enumerate(locators):
        el = try_locator(page, loc)
        if el:
            element = el
            used_locator = loc
            healed = (i > 0)
            break

    if not element:
        return {"status": "failed", "locator_used": None, "error": "No locator matched"}

    try:
        if action_type in ("click", "submit"):
            element.click(timeout=5000)
        elif action_type == "input":
            element.fill(input_value or "", timeout=5000)
        elif action_type == "select":
            element.select_option(input_value, timeout=5000)
        return {"status": "healed" if healed else "passed", "locator_used": used_locator, "error": None}
    except Exception as e:
        return {"status": "failed", "locator_used": used_locator, "error": str(e)[:200]}


def run_execution(test_case_id, target_url, token):
    headers = {"Authorization": f"Bearer {token}"}
    steps_resp = requests.get(f"{API_BASE}/testcases/{test_case_id}/steps", headers=headers)
    steps_resp.raise_for_status()
    steps = steps_resp.json()

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        page = browser.new_page(no_viewport=True)
        page.goto(target_url)
        page.bring_to_front()

        for step in steps:
            time.sleep(0.8)
            result = execute_step(page, step)
            result["step_order"] = step.get("step_order")
            result["description"] = step.get("description")
            results.append(result)
            print(f"Step {step.get('step_order')}: {result['status']} - {step.get('description')}")

        time.sleep(2)
        browser.close()

    passed = sum(1 for r in results if r["status"] == "passed")
    healed = sum(1 for r in results if r["status"] == "healed")
    failed = sum(1 for r in results if r["status"] == "failed")
    overall_status = "failed" if failed > 0 else ("healed" if healed > 0 else "passed")

    resp = requests.post(
        f"{API_BASE}/testcases/{test_case_id}/reports",
        headers=headers,
        json={"status": overall_status, "results": results, "passed": passed, "healed": healed, "failed": failed},
    )
    resp.raise_for_status()
    print(f"Execution complete: {overall_status} ({passed} passed, {healed} healed, {failed} failed)")


if __name__ == "__main__":
    test_case_id = sys.argv[1]
    target_url = sys.argv[2]
    token = sys.argv[3]
    run_execution(test_case_id, target_url, token)