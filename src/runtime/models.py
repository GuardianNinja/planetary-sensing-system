# src/runtime/models.py
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import uuid

class IntentRequest(BaseModel):
    intent_type: str = Field(..., description="High-level intent category")
    payload: Dict[str, Any] = Field(..., description="Structured intent payload")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class NormalizedIntent(BaseModel):
    intent_id: str
    intent_type: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any]

    @classmethod
    def from_request(cls, req: IntentRequest) -> "NormalizedIntent":
        return cls(
            intent_id=str(uuid.uuid4()),
            intent_type=req.intent_type,
            payload=req.payload,
            metadata=req.metadata,
        )

class IntentReceipt(BaseModel):
    intent_id: str
    status: str  # "SUCCESS" | "REJECTED"
    evidence_hash: Optional[str]
    result: Dict[str, Any]
