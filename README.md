AI-Assisted Smart Test Recording and Verification System

An AI-assisted, scriptless web testing platform that records real user actions in a browser, converts them into structured, reusable test cases, and stores every action in a tamper-evident audit log — laying the foundation for automatic self-healing regression testing.

This project is being built in **4 phases over 3 months**. This README currently reflects the status of **Phase 1: Foundation, Scriptless Recorder & Audit-Log Core**.

---

## What This Project Does (in simple words)

Normally, testing a website after every update means a person manually clicking through the same steps again and again, or a QA engineer writing code to automate it. Our system removes both problems:

1. A tester simply **uses the website normally** — clicking buttons, typing in forms, submitting pages.
2. The system **watches and records** every one of those actions in the background.
3. Those actions are automatically turned into a **structured test case** — no code writing required.
4. Every single action taken by the system (creating a user, creating a test case, saving steps) is **permanently logged** in an audit trail that cannot be silently altered, so there's always a verifiable record of what happened and when.

This is the foundation. In later phases, this recorded data will be replayed automatically, verified using AI (text/image similarity), and self-healed when the website's UI changes slightly — without needing to re-record anything.

---

## Why This Matters (the problem we're solving)

Websites change constantly — a button's label changes, an element's ID changes, a layout shifts slightly. When that happens, most automated tests break and need to be rewritten by hand. Our system is being designed so that:

- Recording a test requires **no programming knowledge** — you just use the app.
- Every action is tracked with **multiple ways to find the same element again** (its ID, its visible text, its position), so minor changes don't automatically break things.
- Every change to the system's data is **logged and traceable**, similar to how real audit/compliance systems work in the industry.

---

## Phase 1 — What Has Been Built So Far

Phase 1 focused on proving the two hardest, most important parts of the whole project work reliably: **recording real browser actions**, and **tracking everything in a trustworthy audit log**. Everything below is complete and verified.

### 1. Project Setup
- A clean, organized codebase separating the backend (server), automation (recorder), frontend (user interface, upcoming), and database.
- Version control using Git and GitHub, with every day's work committed and pushed separately — so the full development history is visible and traceable.

### 2. Database Design
- Designed and built 4 core data tables:
  - **Users** — stores tester accounts
  - **TestCases** — stores each recorded test (its name, target website, description)
  - **TestSteps** — stores each individual recorded action (click, type, select, submit), along with multiple ways to re-find that element later
  - **AuditLog** — stores a permanent, timestamped record of every important action taken in the system
- Currently using **SQLite** (a lightweight, file-based database) to build and test quickly without needing external infrastructure. The system is designed so that switching to a production-grade database (like MongoDB Atlas) later is a simple configuration change, not a rewrite — this mirrors how real companies build and test software before scaling it up.

### 3. Secure User Authentication
- Testers can sign up and log in.
- Passwords are never stored in plain text — they are securely hashed using industry-standard encryption (bcrypt).
- Logged-in users receive a secure access token (JWT) that must be presented for any protected action, so the system always knows who is performing each action.

### 4. Tamper-Evident Audit Logging
- Every important action in the system — signing up, logging in, creating a test case, adding test steps — is automatically recorded in the Audit Log.
- Each audit entry is **cryptographically linked to the one before it** (similar to how blockchain records work), meaning if any past entry were ever altered, the chain would visibly break. This makes the log trustworthy evidence of exactly what happened and when — a feature most student projects don't include, and one that mirrors real audit/compliance systems used in the industry.

### 5. Backend API (tested and verified using Postman)
The following working, secured API endpoints have been built and tested:
| Endpoint | Purpose |
|---|---|
| `POST /auth/signup` | Register a new tester account |
| `POST /auth/login` | Log in and receive a secure access token |
| `POST /testcases` | Create a new test case |
| `GET /testcases` | View all saved test cases |
| `POST /testcases/<id>/steps` | Save recorded steps to a test case |

Each of these was manually tested using Postman to confirm correct behavior, including confirming that protected routes correctly reject requests without a valid login token.

### 6. The Scriptless Browser Recorder (the core innovation)
- Built using **Playwright**, an industry-standard browser automation tool.
- When recording starts, a real Chromium browser opens and the tester simply uses the target website normally.
- Every click, text input, dropdown selection, and form submission is automatically captured in the background — with no code required from the tester.
- For every captured action, the system stores **multiple alternative ways to locate that same element again** (its unique ID, its name attribute, its visible text, and its position in the page structure) — this redundancy is what will allow the system to keep working even after minor website changes in a later phase.
- Typing is intelligently captured as a single clean value (e.g., `"standard_user"`) rather than recording every individual keystroke, keeping the recorded data clean and realistic.

### 7. Full End-to-End Pipeline (the proof that everything works together)
A complete real-world test was performed and verified successfully:
1. A tester logs into a demo e-commerce website (SauceDemo).
2. They add products to their cart and complete a full checkout flow.
3. The recorder captures all of this as 20+ structured steps in real time.
4. The recorded session is automatically sent to the backend through a secure, authenticated API call.
5. The test case and all its steps are saved permanently in the database.
6. Every one of these actions is recorded in the audit log.

This proves the entire foundation — **record → structure → authenticate → save → audit** — works correctly, end to end, without any manual data entry.

---

## Technology Used So Far

| Purpose | Technology |
|---|---|
| Backend server & API | Python, Flask |
| Browser automation & recording | Playwright |
| Database (Phase 1 prototype) | SQLite |
| Authentication | JWT + bcrypt |
| API testing | Postman |
| Version control | Git & GitHub |
| Editor | Visual Studio Code |

---

## What's Coming Next (Phases 2–4)

- **Phase 2:** AI-powered verification (checking text and images for correctness using similarity matching) and self-healing — automatically fixing broken test steps when the website changes slightly, instead of failing.
- **Phase 3:** A visual dashboard showing test results, pass/fail trends, and a timeline of every change detected in the target application, running automatically on a schedule.
- **Phase 4:** Full integration testing, automated CI/CD pipeline, security hardening, and deployment to a live, publicly accessible URL.

---

## Project Status
**Phase 1: Complete** — Foundation, scriptless recorder, and tamper-evident audit logging are fully built and verified.
**Timeline:** On schedule, 3-month project, Phase 1 completed within the first week.