"""Intent Interpreter — Convert human intent to structured tasks.

The Intent Interpreter is the first layer of the HI Kernel.
It receives raw human requests and normalizes them into structured
Task objects that the rest of the system can understand.

Blueprint anchor:
"Intent Interpreter: Reads human request, normalizes into structured task."
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid
import time


@dataclass
class IntentPacket:
    """Normalized human intent ready for processing."""
    intent_id: str
    caller_id: str  # Actor ID verified by Identity Spine
    action: str  # What to do
    payload: Dict[str, Any]  # Context and parameters
    signature: str  # Cryptographic signature
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class IntentInterpreter:
    """Converts raw human intent into structured Task objects."""

    def __init__(self):
        self.interpretation_log = []

    def interpret(self, raw_intent: Dict[str, Any]) -> IntentPacket:
        """Interpret raw human request into normalized intent packet.

        Expected raw_intent structure:
        {
            "caller_id": "<actor-id>",
            "action": "<action-name>",
            "payload": { ... },
            "signature": "<signature>"
        }
        """
        # Validate minimal structure
        if not isinstance(raw_intent, dict):
            raise ValueError("Intent must be a dictionary")

        caller_id = raw_intent.get("caller_id")
        action = raw_intent.get("action")
        payload = raw_intent.get("payload", {})
        signature = raw_intent.get("signature")

        if not all([caller_id, action, signature]):
            raise ValueError(
                "Intent must contain: caller_id, action, signature"
            )

        # Normalize payload
        if not isinstance(payload, dict):
            payload = {"value": payload}

        # Create normalized packet
        packet = IntentPacket(
            intent_id=str(uuid.uuid4()),
            caller_id=caller_id,
            action=action,
            payload=payload,
            signature=signature,
            metadata=raw_intent.get("metadata", {}),
        )

        self.interpretation_log.append(
            {
                "intent_id": packet.intent_id,
                "timestamp": packet.timestamp,
                "action": action,
            }
        )

        return packet

    def get_interpretation_log(self) -> list:
        """Retrieve log of all interpretations."""
        return self.interpretation_log
