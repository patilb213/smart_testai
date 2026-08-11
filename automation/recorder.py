from playwright.sync_api import sync_playwright
import json
import time
import os


def record_session(target_url):
    captured_steps = []
    step_counter = {"count": 0}

    def handle_event(event_data):
        step_counter["count"] += 1
        event_data["step_order"] = step_counter["count"]
        event_data["timestamp"] = time.time()
        captured_steps.append(event_data)
        print(f"Captured step {step_counter['count']}: {event_data['action_type']} on {event_data.get('candidate_locators')}")

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
                window.recordEvent({
                    action_type: "click",
                    candidate_locators: getLocators(e.target),
                    page_url: window.location.href
                });
            }, true);

            let inputTimers = new WeakMap();

            document.addEventListener("input", (e) => {
                const el = e.target;
                if (inputTimers.has(el)) {
                    clearTimeout(inputTimers.get(el));
                }
                const timer = setTimeout(() => {
                    window.recordEvent({
                        action_type: "input",
                        candidate_locators: getLocators(el),
                        input_value: el.value,
                        page_url: window.location.href
                    });
                    inputTimers.delete(el);
                }, 600);
                inputTimers.set(el, timer);
            }, true);

            document.addEventListener("change", (e) => {
                if (e.target.tagName === "SELECT") {
                    window.recordEvent({
                        action_type: "select",
                        candidate_locators: getLocators(e.target),
                        input_value: e.target.value,
                        page_url: window.location.href
                    });
                }
            }, true);

            document.addEventListener("submit", (e) => {
                window.recordEvent({
                    action_type: "submit",
                    candidate_locators: getLocators(e.target),
                    page_url: window.location.href
                });
            }, true);
        """)

        page.goto(target_url)

        print(f"Recording started on {target_url}")
        print("Interact with the page. Press Enter in this terminal when done.")
        input()

        browser.close()

    return captured_steps


if __name__ == "__main__":
    steps = record_session("https://www.saucedemo.com")

    output = {
        "name": "SauceDemo Login and Checkout Flow",
        "target_url": "https://www.saucedemo.com",
        "steps": steps
    }

    os.makedirs("automation/recordings", exist_ok=True)
    output_path = "automation/recordings/session_1.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n--- Final Captured Steps ---")
    print(json.dumps(steps, indent=2))
    print(f"\nSaved {len(steps)} steps to {output_path}")