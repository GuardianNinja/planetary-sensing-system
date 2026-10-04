# tests/test_ledger_and_execution_order.py
from fastapi.testclient import TestClient

from src.runtime.app import create_app
from src.runtime.user_world_context import get_user_world_context

client = TestClient(create_app())


def test_ledger_committed_before_execution():
    payload = {
        "intent_type": "demo.order_check",
        "payload": {"message": "check-order"},
        "metadata": {},
    }

    # Prime a fresh world context
    world_ctx = get_user_world_context()
    world_ctx.evidence_cache.clear()

    resp = client.post("/v1/intent", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    intent_id = body["intent_id"]
    evidence_hash = body["evidence_hash"]

    # Ledger must contain pre_execution entry
    entry = world_ctx.evidence_cache.get(intent_id)
    assert entry is not None
    assert entry["phase"] == "pre_execution"
    assert entry["hash"] == evidence_hash
