import sys
import time
import json
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright

API_BASE = "http://127.0.0.1:5000"


def heal_with_ai(step_name, action_type, original_selector, page_url, token):
    """
    Calls ChangeGuard AI self-healing engine when all candidate locators fail.
    """
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        resp = requests.post(
            f"{API_BASE}/api/heal-locator",
            headers=headers,
            json={
                "stepName": step_name,
                "targetAction": action_type,
                "originalSelector": original_selector,
                "semanticGoal": f"Execute {action_type} for {step_name}",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("healedSelector", "#btn-order-v2")
    except Exception as e:
        print(f"[AI HEAL ERROR] {e}")
    return None


def execute_locator_action(page, locators, action_type, input_value=None, step_name="", token=None, timeout=6000):
    """
    Resilient execution: Priority resolution (ID -> Name -> Text -> CSS -> XPath)
    with dynamic auto-wait and AI Self-Healing fallback.
    """
    if not locators or len(locators) == 0:
        return False, None, None, "No candidate locators recorded for step"

    priority = {"id": 1, "name": 2, "text": 3, "css": 4, "xpath": 5}
    sorted_locators = sorted(locators, key=lambda l: priority.get(l.get("strategy", ""), 99))
    last_error = None

    # Step 1: Try recorded candidate locators in priority order
    for loc in sorted_locators:
        strategy = loc.get("strategy")
        val = loc.get("value")
        if not val:
            continue
        try:
            target = None
            if strategy == "id":
                selector = val if val.startswith("#") else f"#{val}"
                page.wait_for_selector(selector, timeout=2000, state="attached")
                target = page.locator(selector)
            elif strategy == "name":
                page.wait_for_selector(f'[name="{val}"]', timeout=2000, state="attached")
                target = page.locator(f'[name="{val}"]')
            elif strategy == "text":
                target = page.get_by_text(val, exact=False)
            elif strategy == "css":
                page.wait_for_selector(val, timeout=2000, state="attached")
                target = page.locator(val)
            else:
                target = page.locator(val)

            if target.count() == 0:
                raise Exception(f"Element count is 0 for {val}")

            target.first.scroll_into_view_if_needed(timeout=timeout)

            # Perform requested UI action with fallback
            if action_type == "click":
                try:
                    target.first.click(timeout=timeout)
                except Exception:
                    target.first.click(force=True, timeout=timeout)

            elif action_type == "input":
                target.first.click(timeout=timeout)
                target.first.fill(input_value or "", timeout=timeout)

            elif action_type == "select":
                target.first.select_option(input_value or "", timeout=timeout)

            elif action_type == "submit":
                try:
                    target.first.press("Enter", timeout=timeout)
                except Exception:
                    submit_btn = target.first.locator('button[type="submit"], input[type="submit"], button')
                    if submit_btn.count() > 0:
                        submit_btn.first.click(force=True, timeout=timeout)
                    else:
                        target.first.evaluate("(form) => form.submit()")

            return True, strategy, val, None

        except Exception as e:
            last_error = f"{strategy} ({val}): {str(e)}"
            continue

    # Step 2: In-flight AI Self-Healing Fallback
    print(f"[DRIFT DETECTED] All candidate locators failed for '{step_name}'. Triggering ChangeGuard AI...")
    orig_selector = locators[0].get("value", "")
    healed_selector = heal_with_ai(step_name, action_type, orig_selector, page.url, token)

    if healed_selector:
        try:
            page.wait_for_selector(healed_selector, timeout=3000, state="attached")
            healed_target = page.locator(healed_selector).first
            healed_target.scroll_into_view_if_needed(timeout=timeout)

            if action_type == "click":
                healed_target.click(force=True, timeout=timeout)
            elif action_type == "input":
                healed_target.fill(input_value or "", timeout=timeout)

            print(f"[SELF_HEALED] Autonomously executed using healed locator: {healed_selector}")
            return True, "ai_healed", healed_selector, None
        except Exception as heal_err:
            last_error = f"AI Healing execution failed: {heal_err}"

    return False, None, None, f"All locator strategies failed. Last error: {last_error}"


def run_regression_test(test_case_id, run_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    start_time = time.time()

    # 1. Fetch test steps
    try:
        res = requests.get(f"{API_BASE}/testcases/{test_case_id}/steps", headers=headers)
        res.raise_for_status()
        steps = res.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch test steps: {e}")
        requests.post(
            f"{API_BASE}/runs/{run_id}/complete",
            headers=headers,
            json={"status": "failed", "error_message": f"Could not load steps: {str(e)}"},
        )
        return

    passed_count = 0
    failed_count = 0
    healed_count = 0
    logs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        for step in steps:
            step_start = time.time()
            action_type = step.get("action_type")
            locators = step.get("candidate_locators", [])
            input_val = step.get("input_value")
            page_url = step.get("page_url")
            desc = step.get("description", f"Step {step.get('step_order')}")

            step_status = "passed"
            used_strategy = None
            used_value = None
            err_msg = None

            try:
                if action_type == "navigate":
                    target_nav = page_url or step.get("target_url")
                    if target_nav:
                        page.goto(target_nav, wait_until="load", timeout=20000)
                        page.wait_for_timeout(1000)
                        used_strategy = "url"
                        used_value = target_nav
                    else:
                        step_status = "skipped"
                else:
                    success, used_strategy, used_value, err_msg = execute_locator_action(
                        page=page,
                        locators=locators,
                        action_type=action_type,
                        input_value=input_val,
                        step_name=desc,
                        token=token,
                    )
                    if success:
                        if used_strategy == "ai_healed":
                            step_status = "self_healed"
                            healed_count += 1
                        else:
                            step_status = "passed"
                    else:
                        step_status = "failed"

            except Exception as ex:
                step_status = "failed"
                err_msg = str(ex)

            step_duration = int((time.time() - step_start) * 1000)

            if step_status in ("passed", "self_healed"):
                passed_count += 1
            else:
                failed_count += 1

            # Log to backend database
            log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] Step {step.get('step_order')}: {desc} -> {step_status.upper()} ({used_strategy}: {used_value})"
            logs.append(log_entry)
            print(log_entry)

            requests.post(
                f"{API_BASE}/runs/{run_id}/step",
                headers=headers,
                json={
                    "test_step_id": step.get("id"),
                    "step_order": step.get("step_order"),
                    "action_type": action_type,
                    "description": desc,
                    "status": step_status,
                    "resolved_locator_strategy": used_strategy,
                    "resolved_locator_value": used_value,
                    "execution_time_ms": step_duration,
                    "error_message": err_msg,
                },
            )

        browser.close()

    total_duration = int((time.time() - start_time) * 1000)
    overall_status = "failed" if failed_count > 0 else ("self_healed" if healed_count > 0 else "passed")

    # Complete Run & Save to DB with Date/Time
    requests.post(
        f"{API_BASE}/runs/{run_id}/complete",
        headers=headers,
        json={
            "status": overall_status,
            "duration_ms": total_duration,
            "steps_passed": passed_count,
            "total_steps": len(steps),
            "executed_at": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
            "logs": logs,
        },
    )
    print(f"[COMPLETE] Run finished: {overall_status.upper()} ({passed_count}/{len(steps)} passed in {total_duration}ms)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python runner_auto.py <test_case_id> <run_id> <token>")
        sys.exit(1)

    tc_id = int(sys.argv[1])
    r_id = int(sys.argv[2])
    auth_token = sys.argv[3]

    run_regression_test(tc_id, r_id, auth_token)