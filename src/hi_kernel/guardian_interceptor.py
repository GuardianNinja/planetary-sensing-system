"""Guardian Interceptor — Triple-guardian pre-kernel evaluation.

The Guardian Interceptor performs the three-gate evaluation:
1. Jarvondis (Structural): Is the request well-formed?
2. Krystal (Clarity): Is the intent semantically clear?
3. Miko (Safety): Does it pass the safety drift gate?

All three must pass for an intent to proceed.

Blueprint anchor:
"Triple-Guardian Pre-Kernel Evaluation.
Guardian Pass Condition: J >= 0.85 AND K >= 0.85 AND M >= 0.85"
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .intent_interpreter import IntentPacket


@dataclass
class GuardianVerdict:
    """Result of triple-guardian evaluation."""
    intent_id: str
    passed: bool
    jarvondis_score: float  # Structural
    krystal_score: float  # Clarity
    miko_score: float  # Safety
    rejection_reason: Optional[str] = None


class GuardianInterceptor:
    """Triple-guardian gate for all intents."""

    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.verdicts_log = []

    def evaluate(self, packet: IntentPacket) -> GuardianVerdict:
        """Run triple-guardian evaluation on intent packet.

        Returns GuardianVerdict with scores for each guardian.
        Intent passes if all three guardians score >= threshold.
        """

        # Gate 1: Jarvondis (Structural Validation)
        j_score = self._jarvondis_check(packet)

        # Gate 2: Krystal (Semantic Clarity)
        k_score = self._krystal_check(packet)

        # Gate 3: Miko (Safety Drift Gate)
        m_score = self._miko_check(packet)

        # Aggregate verdict
        passed = (
            j_score >= self.threshold
            and k_score >= self.threshold
            and m_score >= self.threshold
        )

        rejection_reason = None
        if not passed:
            reasons = []
            if j_score < self.threshold:
                reasons.append(f"Jarvondis structural check failed ({j_score:.2f})")
            if k_score < self.threshold:
                reasons.append(f"Krystal clarity check failed ({k_score:.2f})")
            if m_score < self.threshold:
                reasons.append(f"Miko safety check failed ({m_score:.2f})")
            rejection_reason = " | ".join(reasons)

        verdict = GuardianVerdict(
            intent_id=packet.intent_id,
            passed=passed,
            jarvondis_score=j_score,
            krystal_score=k_score,
            miko_score=m_score,
            rejection_reason=rejection_reason,
        )

        self.verdicts_log.append(
            {
                "intent_id": packet.intent_id,
                "passed": passed,
                "scores": {
                    "jarvondis": j_score,
                    "krystal": k_score,
                    "miko": m_score,
                },
            }
        )

        return verdict

    def _jarvondis_check(self, packet: IntentPacket) -> float:
        """Jarvondis: Structural schema validation.

        Checks:
        - Intent ID is present and non-empty
        - Caller ID is present and non-empty
        - Action is present and non-empty
        - Payload is a dictionary
        - Signature is present
        """
        checks = [
            bool(packet.intent_id),
            bool(packet.caller_id),
            bool(packet.action),
            isinstance(packet.payload, dict),
            bool(packet.signature),
        ]
        return sum(checks) / len(checks)

    def _krystal_check(self, packet: IntentPacket) -> float:
        """Krystal: Semantic clarity check.

        Checks:
        - Action is not ambiguous (word length > 2)
        - Payload is not empty or trivial
        - No conflicting keys in payload
        """
        checks = []

        # Check action clarity
        checks.append(len(packet.action) > 2)

        # Check payload non-triviality
        payload_str = str(packet.payload)
        checks.append(len(payload_str) > 10)

        # Check for obvious conflicts
        has_conflicts = False
        if "action" in packet.payload and packet.payload["action"] != packet.action:
            has_conflicts = True
        checks.append(not has_conflicts)

        return sum(checks) / len(checks) if checks else 0.5

    def _miko_check(self, packet: IntentPacket) -> float:
        """Miko: Safety drift gate.

        Checks:
        - No override_safety flag in payload
        - No bypass_governance flag
        - No dangerous mutations
        - Payload doesn't exceed size limits
        """
        checks = []

        # Reject override attempts
        has_override = "override_safety" in packet.payload
        has_bypass = "bypass_governance" in packet.payload
        checks.append(not has_override and not has_bypass)

        # Check for dangerous actions
        dangerous_actions = [
            "delete_identity",
            "corrupt_ledger",
            "override_kernel",
        ]
        checks.append(packet.action not in dangerous_actions)

        # Check payload size (prevent DOS)
        payload_str = str(packet.payload)
        checks.append(len(payload_str) < 1_000_000)  # 1MB limit

        return sum(checks) / len(checks) if checks else 0.1

    def get_verdicts_log(self) -> list:
        """Retrieve log of all guardian verdicts."""
        return self.verdicts_log
