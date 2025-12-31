# src/models.py
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class StructuralVerdict(str, Enum):
    PASS = "pass_structural"
    SUSPECT = "suspect_structural"
    FAIL = "fail_structural"


class ClarityVerdict(str, Enum):
    CLEAR = "clear"
    AMBIGUOUS = "ambiguous"
    CONTRADICTORY = "contradictory"


class ExperienceVerdict(str, Enum):
    SHARE_NOW = "share_now"
    SHARE_LATER = "share_later_with_context"
    HOLD_FOR_REVIEW = "hold_for_steward_review"


@dataclass
class RawSignal:
    timestamp: float
    node_id: str
    element: str  # "ocean" or "sky"
    payload: Dict[str, Any]


@dataclass
class TripleVerdict:
    structural: StructuralVerdict
    clarity: ClarityVerdict
    experience: ExperienceVerdict
    firewall_state: str  # simple string for now, can be structured later


@dataclass
class VerifiedRecord:
    timestamp: float
    node_id: str
    element: str
    input_payload: Dict[str, Any]
    verdicts: TripleVerdict
