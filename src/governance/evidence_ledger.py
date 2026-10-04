# src/governance/evidence_ledger.py
import hashlib
import json
from typing import Any
from src.runtime.models import NormalizedIntent
from src.runtime.user_world_context import UserWorldContext

class EvidenceLedgerService:
    def __init__(self, world_ctx: UserWorldContext):
        self.world_ctx = world_ctx

    def _hash_intent(self, intent: NormalizedIntent) -> str:
        blob = json.dumps(
            {
                "intent_id": intent.intent_id,
                "intent_type": intent.intent_type,
                "payload": intent.payload,
                "metadata": intent.metadata,
                "enclave": self.world_ctx.local_enclave_id,
            },
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(blob).hexdigest()

    def commit_pre_execution(self, intent: NormalizedIntent) -> str:
        evidence_hash = self._hash_intent(intent)
        # Append to local evidence cache (or durable ledger)
        self.world_ctx.evidence_cache[intent.intent_id] = {
            "phase": "pre_execution",
            "hash": evidence_hash,
        }
        return evidence_hash
