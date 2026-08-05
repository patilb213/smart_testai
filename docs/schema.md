Users
  id, name, email (unique), password_hash, role, created_at

TestCases
  id, name, target_url, description, created_by (FK -> Users.id), created_at, status, version

TestSteps
  id, test_case_id (FK -> TestCases.id), step_order, action_type,
  candidate_locators (JSON list), input_value, page_url, timestamp

AuditLog
  id, action, user, entity_type, entity_id, before_state, after_state,
  ip_address, timestamp, previous_hash, hash