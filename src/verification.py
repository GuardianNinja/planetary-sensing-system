# src/verification.py
from .models import (
    RawSignal,
    StructuralVerdict,
    ClarityVerdict,
    ExperienceVerdict,
    TripleVerdict,
)


class JarvondisVerifier:
    """
    Structural and network logic verifier.
    """

    def verify(self, signal: RawSignal) -> StructuralVerdict:
        # Placeholder rules; extend as needed.
        if not signal.node_id:
            return StructuralVerdict.FAIL

        payload = signal.payload or {}
        # Example sanity check
        if "value" not in payload:
            return StructuralVerdict.SUSPECT

        return StructuralVerdict.PASS


class KrystalVerifier:
    """
    Clarity and pattern verifier.
    """

    def verify(self, signal: RawSignal) -> ClarityVerdict:
        payload = signal.payload or {}
        value = payload.get("value")

        if value is None:
            return ClarityVerdict.CONTRADICTORY

        # Placeholder: simple ranges; customize per sensor type.
        if isinstance(value, (int, float)):
            if -1e6 <= value <= 1e6:
                return ClarityVerdict.CLEAR
            return ClarityVerdict.AMBIGUOUS

        return ClarityVerdict.AMBIGUOUS


class MikoVerifier:
    """
    Experience and human-facing safety verifier.
    """

    def verify(self, signal: RawSignal) -> ExperienceVerdict:
        payload = signal.payload or {}
        severity = payload.get("severity", "normal")

        if severity == "urgent":
            # Might need context to avoid panic; steward review
            return ExperienceVerdict.HOLD_FOR_REVIEW
        if severity == "elevated":
            return ExperienceVerdict.SHARE_LATER
        return ExperienceVerdict.SHARE_NOW


def build_triple_verdict(
    structural: StructuralVerdict,
    clarity: ClarityVerdict,
    experience: ExperienceVerdict,
    firewall_state: str,
) -> TripleVerdict:
    return TripleVerdict(
        structural=structural,
        clarity=clarity,
        experience=experience,
        firewall_state=firewall_state,
    )
