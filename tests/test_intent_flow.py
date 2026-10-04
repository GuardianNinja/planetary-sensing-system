# tests/test_intent_flow.py
import pytest
from fastapi.testclient import TestClient

from src.runtime.app import create_app

client = TestClient(create_app())


def test_v1_intent_golden_path():
    payload = {
        "intent_type": "demo.echo",
        "payload": {"message": "hello, world"},
        "metadata": {"test_case": "golden_path"},
    }

    resp = client.post("/v1/intent", json=payload)
    assert resp.status_code == 200

    body = resp.json()
    # Contract checks
    assert "intent_id" in body
    assert body["status"] == "SUCCESS"
    assert isinstance(body["evidence_hash"], str)
    assert "result" in body

    # Pipeline evidence: task + cocoon + output
    task_result = body["result"]["task_result"]
    assert task_result["status"] == "COMPLETED"
    assert "thread_id" in task_result
    assert "cocoon_id" in task_result
    assert "output" in task_result


def test_v1_intent_rejects_bad_payload():
    # Missing required fields → Pydantic / FastAPI should reject
    resp = client.post("/v1/intent", json={"payload": {}})
    assert resp.status_code == 422  # validation error
