"""
slos_kernel/orchestrator_bridge.py
Wires src/firewall.py directly into the HI Kernel Request Pipeline.
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple
from src.firewall import (
    GyroscopicFirewall, 
    ConfidenceScores, 
    BeadRuleContext, 
    QRAuthContext
)

class GovernedRequestPipeline:
    def __init__(self, firewall: GyroscopicFirewall):
        self.firewall = firewall
        self.step_counter = 0

    def process_intent(
        self, 
        raw_intent: Dict[str, Any],
        guardian_evals: Tuple[float, float, float], # (Jarvondis, Krystal, Miko)
        bead_ctx: BeadRuleContext = None,
        qr_ctx: QRAuthContext = None
    ) -> Dict[str, Any]:
        self.step_counter += 1
        
        # 1. Map raw Guardian outputs to Firewall Confidence
        scores = ConfidenceScores(
            structural_confidence=guardian_evals[0],
            clarity_confidence=guardian_evals[1],
            human_safety_confidence=guardian_evals[2]
        )

        # 2. Advance Firewall state
        state = self.firewall.next_state(step=self.step_counter, confidence=scores)

        # 3. Filter intent through Gyroscopic Firewall
        enriched_signal = self.firewall.filter_signal(
            signal=raw_intent,
            state=state,
            bead_ctx=bead_ctx,
            qr_ctx=qr_ctx
        )

        # 4. Enforce consensus rules
        needs_fallback = self.firewall.requires_multi_model_and_identity(
            confidence=scores,
            models_validated=3 if scores.aggregate() >= 0.8 else 1,
            identities_validated=1 if bead_ctx or qr_ctx else 0
        )

        if needs_fallback or enriched_signal["_firewall_decision"] != "ALLOW":
            enriched_signal["_pipeline_status"] = "BLOCKED_FOR_REVIEW"
            enriched_signal["_dispatch_ready"] = False
        else:
            enriched_signal["_pipeline_status"] = "CLEARED_FOR_DISPATCH"
            enriched_signal["_dispatch_ready"] = True

        return enriched_signal
