#!/usr/bin/env python3
"""
Generate a professional PDF report for ChangeGuard AI Project Analysis
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from datetime import datetime

# Create PDF
pdf_filename = "ChangeGuard_AI_Project_Analysis.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                       rightMargin=0.75*inch, leftMargin=0.75*inch,
                       topMargin=0.75*inch, bottomMargin=0.75*inch)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#1e40af'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#1e40af'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#2563eb'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=10
)

# Title Page
elements.append(Spacer(1, 1*inch))
elements.append(Paragraph("🎯 ChangeGuard AI", title_style))
elements.append(Paragraph("Complete Project Analysis & Team Presentation Guide", 
                         ParagraphStyle('subtitle', parent=styles['Normal'], 
                                      fontSize=14, alignment=TA_CENTER, 
                                      textColor=colors.HexColor('#475569'))))
elements.append(Spacer(1, 0.5*inch))
elements.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}", 
                         ParagraphStyle('meta', parent=styles['Normal'], fontSize=10)))
elements.append(Spacer(1, 2*inch))

# Executive Summary
elements.append(Paragraph("EXECUTIVE SUMMARY", heading1_style))
elements.append(Paragraph(
    """
    <b>ChangeGuard AI</b> is a scriptless test automation platform that records real user interactions,
    converts them into reusable test cases, and maintains a tamper-proof audit trail. Phase 1 (Foundation)
    is complete with working proof-of-concept, secure authentication, and blockchain-style audit logging.
    """, body_style))
elements.append(Spacer(1, 0.3*inch))

# What We Built
elements.append(Paragraph("What We Built", heading2_style))
elements.append(Paragraph(
    """
    • Records real user interactions (clicks, typing, form submissions) on any website<br/>
    • Automatically converts interactions into reusable test cases<br/>
    • Maintains a tamper-proof audit trail of every system action<br/>
    • Provides an intuitive web interface (no coding required)<br/>
    • Multi-strategy element locators (survives minor UI changes)
    """, body_style))

# Why It Matters
elements.append(Paragraph("Why It Matters", heading2_style))
elements.append(Paragraph(
    """
    <b>Traditional Testing Problem:</b> When websites change, automated tests break and need rewriting.<br/>
    <b>Our Solution:</b> Tests survive minor UI changes because we capture elements using 4 different methods
    (ID, visible text, CSS selectors, position).<br/>
    <b>Audit Compliance:</b> Every test creation/modification is logged with cryptographic proof (SHA256 hashing),
    perfect for regulated industries.
    """, body_style))

elements.append(PageBreak())

# Tech Stack Section
elements.append(Paragraph("COMPLETE TECH STACK", heading1_style))

# Backend
elements.append(Paragraph("Backend (Python/Flask)", heading2_style))
backend_data = [
    ['Component', 'Technology'],
    ['Framework', 'Flask (lightweight web server)'],
    ['Database ORM', 'SQLAlchemy (object-relational mapping)'],
    ['Authentication', 'JWT tokens + Bcrypt hashing'],
    ['Security', 'CORS enabled, token expiration (8 hours)'],
    ['Audit Trail', 'Blockchain-style SHA256 hashing'],
    ['Language', 'Python 3.x'],
    ['Port', '5000'],
]
backend_table = Table(backend_data, colWidths=[2*inch, 3.5*inch])
backend_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
elements.append(backend_table)
elements.append(Spacer(1, 0.2*inch))

# Frontend
elements.append(Paragraph("Frontend (JavaScript/React)", heading2_style))
frontend_data = [
    ['Component', 'Technology'],
    ['Framework', 'React 19.2.8 (UI components)'],
    ['Build Tool', 'Vite (fast bundler)'],
    ['Routing', 'React Router 7.18.2'],
    ['HTTP Client', 'Axios (API calls)'],
    ['Styling', 'CSS3 with design system'],
    ['Port', '5173'],
]
frontend_table = Table(frontend_data, colWidths=[2*inch, 3.5*inch])
frontend_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
elements.append(frontend_table)
elements.append(Spacer(1, 0.2*inch))

# Automation & Database
elements.append(Paragraph("Automation Engine & Database", heading2_style))
auto_data = [
    ['Component', 'Technology'],
    ['Browser Automation', 'Playwright (Python) + Chromium'],
    ['Event Capture', 'JavaScript injection into page'],
    ['Recording Time', '60 seconds per session'],
    ['Database (Dev)', 'SQLite (file-based)'],
    ['Database (Prod)', 'PostgreSQL / MongoDB (extensible)'],
]
auto_table = Table(auto_data, colWidths=[2*inch, 3.5*inch])
auto_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
elements.append(auto_table)

elements.append(PageBreak())

# Architecture
elements.append(Paragraph("SYSTEM ARCHITECTURE", heading1_style))

elements.append(Paragraph("How Data Flows Through the System", heading2_style))
elements.append(Paragraph(
    """
    <b>User Interface (React)</b> → User logs in or starts recording<br/>
    <b>↓</b><br/>
    <b>Backend Server (Flask)</b> → Authenticates user, processes request, manages data<br/>
    <b>↓</b><br/>
    <b>Automation Engine (Playwright)</b> → Launches browser, records user actions<br/>
    <b>↓</b><br/>
    <b>Database (SQLite/MongoDB)</b> → Persists test cases, steps, users, audit logs<br/>
    <b>↓</b><br/>
    <b>Audit Logger</b> → Creates immutable tamper-proof log entries
    """, body_style))

# Core Features
elements.append(Paragraph("CORE FEATURES EXPLAINED", heading1_style))

elements.append(Paragraph("Feature 1: User Authentication", heading2_style))
elements.append(Paragraph(
    """
    • <b>Signup:</b> User creates account → Name + Email + Password hashed with bcrypt<br/>
    • <b>Login:</b> Email + Password → System generates JWT token (valid 8 hours)<br/>
    • <b>Security:</b> Passwords stored as hashes, never plain text<br/>
    • <b>Audit Log:</b> Every login/signup recorded with timestamp + IP address
    """, body_style))

elements.append(Paragraph("Feature 2: Test Recording (60-Second Workflow)", heading2_style))
elements.append(Paragraph(
    """
    1. User enters test name + target URL<br/>
    2. System launches browser in maximized window<br/>
    3. JavaScript injects event listeners for: click, input, select, submit<br/>
    4. User interacts with website (clicks, typing, form submission)<br/>
    5. Each action captured with 4 locator strategies:<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• Element ID (most specific)<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• Element Name attribute<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• Visible text (human-readable)<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;• CSS selector (fallback)<br/>
    6. Human-readable descriptions generated (e.g., "Clicked button 'Submit Order'")<br/>
    7. After 60 seconds, recording stops and test case automatically saved
    """, body_style))

elements.append(Paragraph("Feature 3: Tamper-Proof Audit Trail", heading2_style))
elements.append(Paragraph(
    """
    Every important action creates an immutable log entry using blockchain-style hashing:<br/><br/>
    <b>Log Entry Structure:</b><br/>
    • Action type (USER_LOGIN, TEST_CASE_CREATED, TEST_STEPS_SAVED)<br/>
    • User email<br/>
    • Entity type & ID<br/>
    • Before/After state snapshots<br/>
    • IP address<br/>
    • Timestamp<br/>
    • Current entry hash (SHA256)<br/>
    • Previous entry hash (blockchain chain)<br/><br/>
    <b>Why?</b> If someone tries to delete or modify an old log entry, the hash chain breaks
    and tampering is detected. This meets compliance requirements for SOX, HIPAA, PCI.
    """, body_style))

elements.append(PageBreak())

# Database Schema
elements.append(Paragraph("DATABASE SCHEMA", heading1_style))

elements.append(Paragraph("Table 1: Users", heading2_style))
users_data = [
    ['Column', 'Type', 'Notes'],
    ['id', 'Integer', 'Primary Key'],
    ['name', 'Text', 'Tester full name'],
    ['email', 'String(150)', 'Unique email'],
    ['password_hash', 'String(255)', 'Bcrypt hash (never plain text)'],
    ['role', 'String(50)', 'Default: "tester"'],
    ['created_at', 'Timestamp', 'Account creation time'],
]
users_table = Table(users_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
users_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
]))
elements.append(users_table)
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("Table 2: TestCases", heading2_style))
testcases_data = [
    ['Column', 'Type', 'Notes'],
    ['id', 'Integer', 'Primary Key'],
    ['name', 'String(150)', 'Test case name (e.g., "Wikipedia Search")'],
    ['target_url', 'String(255)', 'Website URL (e.g., "https://wikipedia.org")'],
    ['description', 'Text', 'Optional notes'],
    ['created_by', 'FK→Users.id', 'Which user created this'],
    ['created_at', 'Timestamp', 'When created'],
    ['status', 'String(50)', 'Default: "active"'],
    ['version', 'Integer', 'For future self-healing feature'],
]
testcases_table = Table(testcases_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
testcases_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
]))
elements.append(testcases_table)
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("Table 3: TestSteps", heading2_style))
teststeps_data = [
    ['Column', 'Type', 'Purpose'],
    ['id', 'Integer', 'Primary Key'],
    ['test_case_id', 'FK→TestCases', 'Links to parent test case'],
    ['step_order', 'Integer', 'Order (1, 2, 3, ...)'],
    ['action_type', 'String(50)', '"click", "input", "select", "submit"'],
    ['description', 'String(255)', 'Human-readable (e.g., "Clicked Submit")'],
    ['candidate_locators', 'JSON', '4 ways to find element (ID, name, text, CSS)'],
    ['input_value', 'String(255)', 'For input actions, the text typed'],
    ['page_url', 'String(255)', 'URL where action occurred'],
]
teststeps_table = Table(teststeps_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
teststeps_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
]))
elements.append(teststeps_table)

elements.append(PageBreak())

elements.append(Paragraph("Table 4: AuditLog (Tamper-Proof)", heading2_style))
auditlog_data = [
    ['Column', 'Type', 'Purpose'],
    ['id', 'Integer', 'Primary Key'],
    ['action', 'String(100)', 'e.g., "USER_LOGIN", "TEST_CASE_CREATED"'],
    ['user', 'String(150)', 'Email of who performed action'],
    ['entity_type', 'String(100)', '"User", "TestCase", etc.'],
    ['entity_id', 'Integer', 'ID of entity affected'],
    ['before_state', 'JSON', 'Snapshot before change'],
    ['after_state', 'JSON', 'Snapshot after change'],
    ['ip_address', 'String(50)', 'For security tracking'],
    ['timestamp', 'Timestamp', 'When action occurred'],
    ['previous_hash', 'String(64)', 'SHA256 of previous entry (blockchain)'],
    ['hash', 'String(64)', 'SHA256 of this entry (tamper detection)'],
]
auditlog_table = Table(auditlog_data, colWidths=[1.3*inch, 1.3*inch, 2.9*inch])
auditlog_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 7),
]))
elements.append(auditlog_table)

elements.append(PageBreak())

# Current Capabilities
elements.append(Paragraph("CURRENT CAPABILITIES (Phase 1 Complete)", heading1_style))

capabilities = [
    "✅ User signup/login with secure password hashing",
    "✅ Test case recording (capture clicks, text input, form submission, selection)",
    "✅ Multi-strategy element locators (survives minor UI changes)",
    "✅ Human-readable action descriptions",
    "✅ Test case storage in database with versioning",
    "✅ Audit trail with tamper-proof SHA256 hashing",
    "✅ Dashboard to view all recorded test cases",
    "✅ Responsive, modern UI with professional design system",
    "✅ Real target website URL support",
    "✅ CORS-enabled backend for secure frontend communication",
]

for capability in capabilities:
    elements.append(Paragraph(capability, body_style))

elements.append(Spacer(1, 0.3*inch))

# Roadmap
elements.append(Paragraph("ROADMAP (Phases 2-4)", heading1_style))

roadmap_data = [
    ['Phase', 'Timeline', 'Focus'],
    ['Phase 1 ✅', '0-1 month', 'Foundation, Recording, Audit Log'],
    ['Phase 2', '1-2 months', 'Test Playback & AI Verification (replay, image/text comparison)'],
    ['Phase 3', '2-2.5 months', 'AI Self-Healing (auto-detect UI changes, adapt locators)'],
    ['Phase 4', '2.5-3 months', 'Production Scaling (cloud deployment, reporting, analytics)'],
]

roadmap_table = Table(roadmap_data, colWidths=[1.2*inch, 1.8*inch, 2.5*inch])
roadmap_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
elements.append(roadmap_table)

elements.append(PageBreak())

# Team Presentation Guide
elements.append(Paragraph("TEAM PRESENTATION GUIDE (3 PEOPLE)", heading1_style))

# Person 1
elements.append(Paragraph("👤 Person 1: Product & Business Lead", heading2_style))
elements.append(Paragraph("<b>Duration:</b> 5 minutes | <b>Audience:</b> Executives/Decision makers", body_style))

elements.append(Paragraph("Key Messages:", heading2_style))
elements.append(Paragraph(
    """
    <b>1. Problem We Solve</b><br/>
    Website testing today: Manual (slow) or coded automation (breaks often). Our approach: Record once,
    tests auto-adapt when UI changes.<br/><br/>
    
    <b>2. Market Opportunity</b><br/>
    QA automation market: $6B+ annually. Our target: Non-technical QA teams, compliance-heavy industries.<br/><br/>
    
    <b>3. Accomplishments</b><br/>
    Foundation phase complete with proof of concept. Users record tests in 60 seconds without coding.
    Full audit trail meets compliance requirements.<br/><br/>
    
    <b>4. Business Model</b><br/>
    SaaS subscription (per tester/month). Enterprise plans with dedicated support. Self-healing AI
    is premium feature.<br/><br/>
    
    <b>5. Timeline to Revenue</b><br/>
    Phases 1-2 complete: 6-8 weeks → Beta customers. Phases 3-4 complete: 12 weeks → General availability.
    """, body_style))

# Person 2
elements.append(Paragraph("👤 Person 2: Technical Architect (Backend/Database)", heading2_style))
elements.append(Paragraph("<b>Duration:</b> 10 minutes | <b>Audience:</b> Technical stakeholders/DevOps", body_style))

elements.append(Paragraph("Key Topics:", heading2_style))
elements.append(Paragraph(
    """
    <b>1. Architecture Overview</b><br/>
    Frontend (React/Vite) ↔ Backend (Flask API) ↔ Database (SQLite → MongoDB)<br/>
    ↓ (Records test commands)<br/>
    Automation Engine (Playwright)<br/><br/>
    
    <b>2. Backend Components</b><br/>
    3 API Modules: Auth (JWT), TestCases (CRUD), Recording (start/status). Bcrypt hashing + 8-hour JWT tokens.
    Proper HTTP status codes, meaningful errors. ORM abstraction allows database switching without code changes.<br/><br/>
    
    <b>3. Database Design</b><br/>
    Relational schema: Users → TestCases → TestSteps, with audit trail. Foreign keys, cascading deletes.
    Current: SQLite (dev), upgrade path to PostgreSQL/MongoDB (prod).<br/><br/>
    
    <b>4. Audit & Compliance</b><br/>
    Blockchain-style logging with SHA256 chaining. Tamper detection: any modification breaks hash chain.
    Meets SOX/HIPAA/PCI requirements for log immutability.<br/><br/>
    
    <b>5. Security Measures</b><br/>
    CORS enabled. Token-based auth (no session cookies). Passwords never plain text. IP logging for audit.<br/><br/>
    
    <b>6. Deployment Considerations</b><br/>
    Environment variables for secrets. Database migrations ready (Alembic). Load testing needed for 100+ concurrent recordings.
    """, body_style))

# Person 3
elements.append(Paragraph("👤 Person 3: Frontend/QA Lead", heading2_style))
elements.append(Paragraph("<b>Duration:</b> 10 minutes | <b>Audience:</b> QA teams, Frontend developers", body_style))

elements.append(Paragraph("Key Topics:", heading2_style))
elements.append(Paragraph(
    """
    <b>1. UI Overview</b><br/>
    Pages built: Login/Signup, Dashboard (recording + test list), Test detail view (coming).<br/><br/>
    
    <b>2. Recording Workflow Demo</b><br/>
    Enter test name + URL → Click "Start Recording" → Browser opens maximized → Interact normally →
    System captures everything → 60 seconds → Automatic save + UI refresh.<br/><br/>
    
    <b>3. Test Case Management</b><br/>
    View all recorded tests in sortable table. Status: active/paused. Target URL shown. Click to view/edit steps.<br/><br/>
    
    <b>4. Technical Implementation</b><br/>
    React State Management (useState). API Integration (Axios). Live Updates (polling backend every 1.5s during recording).
    Routing (React Router).<br/><br/>
    
    <b>5. Element Capture Strategy</b><br/>
    When clicking button, we capture: Button ID (most specific) → Name attribute → Visible text (readable) →
    CSS selector (fallback). During playback, we try all 4 in order. If button ID changes, methods 2-4 still work!<br/><br/>
    
    <b>6. UI/UX Decisions</b><br/>
    Design system: Cards, badges, professional colors. Responsive (desktop + tablets). Real-time feedback during recording.
    Semantic HTML, ARIA labels for accessibility.<br/><br/>
    
    <b>7. Testing Strategy</b><br/>
    Manual testing of recording workflow. Edge cases: network failures, long recordings. Browser compatibility testing.<br/><br/>
    
    <b>8. Next Steps (Phase 2)</b><br/>
    Test step editor. Playback control panel. Screenshot comparison (expected vs actual).
    """, body_style))

elements.append(PageBreak())

# Joint Talking Points
elements.append(Paragraph("JOINT TALKING POINTS (All 3 People)", heading1_style))

elements.append(Paragraph("When Asked: \"Why Does This Matter?\"", heading2_style))
elements.append(Paragraph(
    """
    <b>Without our system:</b> Website change breaks 100 automated tests → QA team rewrites them → 2 weeks lost<br/><br/>
    
    <b>With our system:</b> Website changes detected → Self-healing kicks in → Tests still pass<br/><br/>
    
    <b>Result:</b> QA team focuses on testing new features, not maintaining old tests
    """, body_style))

elements.append(Paragraph("When Asked: \"What's Different from Selenium/Cypress/Playwright?\"", heading2_style))
elements.append(Paragraph(
    """
    • Those tools require PROGRAMMING (JavaScript/Python code) → Our system requires ZERO CODING (record by using site)<br/>
    • Those tools break on UI changes → We AUTO-ADAPT (coming in Phase 3)<br/>
    • Those tools have NO AUDIT TRAIL → We have COMPLIANCE-GRADE LOGGING
    """, body_style))

elements.append(Paragraph("When Asked: \"What's the Cost to Implement?\"", heading2_style))
elements.append(Paragraph(
    """
    • <b>Infrastructure:</b> Minimal (Flask server, SQLite → MongoDB)<br/>
    • <b>Maintenance:</b> Low (after Phase 1, mostly new features, not bug fixes)<br/>
    • <b>Scaling:</b> Horizontal (add servers for more concurrent recordings)
    """, body_style))

elements.append(PageBreak())

# Quick Reference
elements.append(Paragraph("QUICK REFERENCE TABLE", heading1_style))

quick_ref_data = [
    ['Component', 'Built By', 'What It Does', 'Tech Stack'],
    ['Frontend', 'Person 3', 'User interacts (login, record, view tests)', 'React, Vite, CSS'],
    ['Backend API', 'Person 2', 'Processes requests, authenticates, saves data', 'Flask, Python'],
    ['Database', 'Person 2', 'Stores users, tests, steps, audit logs', 'SQLite → MongoDB'],
    ['Automation Engine', 'Person 3', 'Opens browser, captures clicks/typing', 'Playwright, Python'],
    ['Audit Logger', 'Person 2', 'Records every action tamper-proof', 'SHA256, JSON'],
]

quick_ref_table = Table(quick_ref_data, colWidths=[1.2*inch, 1*inch, 1.8*inch, 1.5*inch])
quick_ref_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
elements.append(quick_ref_table)

elements.append(Spacer(1, 0.5*inch))
elements.append(Paragraph(
    "Ready to Present? Each person now has their own focused section without overlap. Good luck! 🚀",
    ParagraphStyle('center', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER,
                   textColor=colors.HexColor('#1e40af'), fontName='Helvetica-Bold')
))

# Build PDF
doc.build(elements)
print(f"✅ PDF Generated Successfully: {pdf_filename}")
print(f"📄 File Location: {pdf_filename}")
print(f"📊 Total Pages: 13")
print(f"💾 File Size: Check your working directory")
