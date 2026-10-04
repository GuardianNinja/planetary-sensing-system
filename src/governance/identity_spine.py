# src/governance/identity_spine.py
from typing import Dict, Any

class IdentitySpine:
    def __init__(self, identity: Dict[str, Any]):
        self.identity = identity

    def resolve_subject(self) -> str:
        return self.identity.get("user_id", "unknown")

    def resolve_lanes(self) -> Dict[str, Any]:
        return {"lane": "default"}
