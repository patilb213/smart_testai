import axios from "axios";

const API_BASE = "http://127.0.0.1:5000";

export const login = (email, password) =>
  axios.post(`${API_BASE}/auth/login`, { email, password });

export const signup = (name, email, password) =>
  axios.post(`${API_BASE}/auth/signup`, { name, email, password });

export const getTestCases = (token) =>
  axios.get(`${API_BASE}/testcases`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const getStepsForTestCase = (token, testCaseId) =>
  axios.get(`${API_BASE}/testcases/${testCaseId}/steps`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const runTestCase = (token, testCaseId) =>
  axios.post(
    `${API_BASE}/runs/start`,
    { test_case_id: testCaseId },
    { headers: { Authorization: `Bearer ${token}` } }
  );
export const getTestRuns = (token, testCaseId) =>
  axios.get(`${API_BASE}/runs/testcase/${testCaseId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
export const getRunDetail = (token, runId) =>
  axios.get(`${API_BASE}/runs/${runId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
export const getChangeEvents = (token, testCaseId) =>
  axios.get(`${API_BASE}/runs/testcase/${testCaseId}/changes`, {
    headers: { Authorization: `Bearer ${token}` },
  });