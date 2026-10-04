# src/runtime/user_world_context.py
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class UserWorldContext:
    identity: Dict[str, Any]
    lane: str
    safety_profile: Dict[str, Any]
    evidence_cache: Dict[str, Any]
    local_enclave_id: str

def get_user_world_context() -> UserWorldContext:
    # In real runtime, derive from auth headers, tokens, or local config.
    return UserWorldContext(
        identity={"user_id": "demo-user"},
        lane="default",
        safety_profile={"max_risk": "LOW"},
        evidence_cache={},
        local_enclave_id="enclave-001",
    )
