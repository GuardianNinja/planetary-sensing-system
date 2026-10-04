# src/firewall.py
import random
import time
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable


GYRO_AXES = ["identity_focus", "route_focus", "anomaly_focus"]


# -------------------------------------------------------------------
# DATA STRUCTURES
# -------------------------------------------------------------------
@dataclass
class AxisWeights:
    """
    Per-axis weighting for emphasis.
    Values are normalized or interpreted by higher layers.
    """
    identity_focus: float = 1.0
    route_focus: float = 1.0
    anomaly_focus: float = 1.0


@dataclass
class ConfidenceScores:
    """
    Confidence scores derived from upstream models / checks.
    These are *inputs* from Jarvondis/Krystal/Miko or other guardians.
    """
    structural_confidence: float = 0.0   # Jarvondis
    clarity_confidence: float = 0.0      # Krystal
    human_safety_confidence: float = 0.0 # Miko

    def aggregate(self) -> float:
        # Simple average; can be replaced with weighted logic.
        return (
            self.structural_confidence
            + self.clarity_confidence
            + self.human_safety_confidence
        ) / 3.0


@dataclass
class LedgerEntry:
    """
    Minimal ledger binding for firewall decisions.
    In a real system, this would be hash-chained and persisted.
    """
    timestamp: float
    axis: str
    seed: int
    axis_weight: float
    aggregate_confidence: float
    decision: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FirewallState:
    axis: str
    seed: int
    axis_weights: AxisWeights
    confidence: ConfidenceScores
    fallback_used: bool = False


# -------------------------------------------------------------------
# BEAD RULE / QR LAYER PLACEHOLDERS
# -------------------------------------------------------------------
@dataclass
class BeadRuleContext:
    """
    Placeholder for bead-based rule integration.
    Could include band/bead/bracelet identity artifacts, etc.
    """
    bead_id: Optional[str] = None
    band_type: Optional[str] = None
    lineage_tag: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QRAuthContext:
    """
    Placeholder for QR-based rotating code authentication.
    """
    qr_id: Optional[str] = None
    rotating_code: Optional[str] = None
    valid_until: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)


# -------------------------------------------------------------------
# GYROSCOPIC FIREWALL
# -------------------------------------------------------------------
class GyroscopicFirewall:
    """
    Conceptual gyroscopic firewall v2.

    - Rotates emphasis across axes over time.
    - Applies axis weights.
    - Consumes confidence scores from upstream guardians.
    - Binds decisions into a simple in-memory ledger.
    - Integrates bead rules and QR-based auth context.
    - Provides fallback logic when confidence is insufficient.
    """

    def __init__(
        self,
        base_seed: int = 42,
        axis_weights: Optional[AxisWeights] = None,
        ledger_sink: Optional[Callable[[LedgerEntry], None]] = None,
        fallback_threshold: float = 0.6,
    ):
        self.base_seed = base_seed
        self._rng = random.Random(base_seed)
        self.axis_weights = axis_weights or AxisWeights()
        self.ledger: List[LedgerEntry] = []
        self.ledger_sink = ledger_sink
        self.fallback_threshold = fallback_threshold

    # -----------------------------
    # STATE ROTATION
    # -----------------------------
    def next_state(
        self,
        step: int,
        confidence: Optional[ConfidenceScores] = None,
    ) -> FirewallState:
        axis = GYRO_AXES[step % len(GYRO_AXES)]
        seed = self._rng.randint(0, 1_000_000)
        confidence = confidence or ConfidenceScores()

        return FirewallState(
            axis=axis,
            seed=seed,
            axis_weights=self.axis_weights,
            confidence=confidence,
            fallback_used=False,
        )

    # -----------------------------
    # CORE FILTER + DECISION
    # -----------------------------
    def filter_signal(
        self,
        signal: Dict[str, Any],
        state: FirewallState,
        bead_ctx: Optional[BeadRuleContext] = None,
        qr_ctx: Optional[QRAuthContext] = None,
    ) -> Dict[str, Any]:
        """
        Annotate signals with firewall metadata and make a simple decision.

        In a real system, this would:
        - enforce policies,
        - consult bead rules,
        - validate QR rotating codes,
        - and bind decisions into a cryptographic ledger.
        """

        enriched = dict(signal)

        # Axis emphasis
        axis_weight = getattr(state.axis_weights, state.axis, 1.0)
        aggregate_conf = state.confidence.aggregate()

        # Simple decision logic:
        # - If confidence is high enough, allow with emphasis.
        # - If not, trigger fallback and mark for stricter upstream review.
        decision = "ALLOW"
        fallback_used = False

        if aggregate_conf < self.fallback_threshold:
            decision = "FALLBACK_REVIEW"
            fallback_used = True

        # Attach firewall metadata
        enriched["_firewall_axis"] = state.axis
        enriched["_firewall_seed"] = state.seed
        enriched["_firewall_axis_weight"] = axis_weight
        enriched["_firewall_confidence_structural"] = state.confidence.structural_confidence
        enriched["_firewall_confidence_clarity"] = state.confidence.clarity_confidence
        enriched["_firewall_confidence_human_safety"] = state.confidence.human_safety_confidence
        enriched["_firewall_confidence_aggregate"] = aggregate_conf
        enriched["_firewall_decision"] = decision
        enriched["_firewall_fallback_used"] = fallback_used

        # Bead rule + QR context (placeholders)
        if bead_ctx:
            enriched["_bead_ctx"] = {
                "bead_id": bead_ctx.bead_id,
                "band_type": bead_ctx.band_type,
                "lineage_tag": bead_ctx.lineage_tag,
                "extra": bead_ctx.extra,
            }

        if qr_ctx:
            enriched["_qr_ctx"] = {
                "qr_id": qr_ctx.qr_id,
                "rotating_code": qr_ctx.rotating_code,
                "valid_until": qr_ctx.valid_until,
                "extra": qr_ctx.extra,
            }

        # Ledger binding
        ledger_entry = LedgerEntry(
            timestamp=time.time(),
            axis=state.axis,
            seed=state.seed,
            axis_weight=axis_weight,
            aggregate_confidence=aggregate_conf,
            decision=decision,
            metadata={
                "fallback_used": fallback_used,
                "bead_present": bead_ctx is not None,
                "qr_present": qr_ctx is not None,
            },
        )
        self._bind_ledger(ledger_entry)

        return enriched

    # -----------------------------
    # LEDGER HANDLING
    # -----------------------------
    def _bind_ledger(self, entry: LedgerEntry) -> None:
        """
        Bind firewall decisions into an in-memory ledger.
        In production, this would be hash-chained and persisted.
        """
        self.ledger.append(entry)
        if self.ledger_sink:
            self.ledger_sink(entry)

    # -----------------------------
    # FALLBACK LOGIC (EXPLICIT)
    # -----------------------------
    def requires_multi_model_and_identity(
        self,
        confidence: ConfidenceScores,
        models_validated: int,
        identities_validated: int,
    ) -> bool:
        """
        Explicit helper to express your 'three reasonable models + one to two people' rule.

        Returns True if:
        - aggregate confidence is below threshold, OR
        - fewer than 3 validated models, OR
        - fewer than 1 validated identity.
        """
        aggregate_conf = confidence.aggregate()
        if aggregate_conf < self.fallback_threshold:
            return True
        if models_validated < 3:
            return True
        if identities_validated < 1:
            return True
        return False
