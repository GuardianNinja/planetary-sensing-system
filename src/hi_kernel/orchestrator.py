"""HI Kernel Orchestrator — Unified brainstem engine.

The orchestrator coordinates the complete request pipeline:
1. Intent interpretation
2. Guardian evaluation
3. Governance verification
4. Evidence logging
5. Arach dispatch
6. Result recombination

Blueprint anchor:
"HI → Guardian → Governance → Evidence → Arach → Result"
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time

from .intent_interpreter import IntentInterpreter, IntentPacket
from .guardian_interceptor import GuardianInterceptor


@dataclass
class ExecutionReceipt:
    """Governed execution receipt returned to caller."""
    intent_id: str
    status: str  # "SUCCESS" or "REJECTED"
    evidence_hash: str
    result: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)


class HIKernelOrchestrator:
    """Unified brainstem orchestrating the complete request pipeline."""

    def __init__(
        self,
        governance_enforcer: Any,  # From src.governance
        arach_dispatcher: Any,  # From src.task_spider
        guardian_threshold: float = 0.85,
    ):
        self.governance = governance_enforcer
        self.arach = arach_dispatcher
        self.intent_interpreter = IntentInterpreter()
        self.guardian_interceptor = GuardianInterceptor(threshold=guardian_threshold)
        self.execution_log = []

    def process_intent(self, raw_intent: Dict[str, Any]) -> ExecutionReceipt:
        """Process a raw intent through the complete pipeline.

        Pipeline:
        1. IntentInterpreter: normalize raw intent
        2. GuardianInterceptor: triple-guardian evaluation
        3. GovernanceEnforcer: verify identity + permissions + safety
        4. EvidenceLedger: log approved intent
        5. ArachDispatcher: execute in user world enclave
        6. RecombinationLayer: validate + merge results

        Returns ExecutionReceipt with status and result.
        """

        # Stage 1: Intent Interpretation
        try:
            packet = self.intent_interpreter.interpret(raw_intent)
        except ValueError as e:
            return ExecutionReceipt(
                intent_id="unknown",
                status="REJECTED",
                evidence_hash="",
                result={"error": f"Intent interpretation failed: {str(e)}"},
            )

        # Stage 2: Guardian Interceptor (Triple-Guardian)
        guardian_verdict = self.guardian_interceptor.evaluate(packet)
        if not guardian_verdict.passed:
            # Log rejection to evidence ledger
            evidence_record = self.governance.evidence_ledger.append(
                event_type="VERIFICATION_FAILED",
                actor_id=packet.caller_id,
                intent_id=packet.intent_id,
                payload={
                    "action": packet.action,
                    "jarvondis": guardian_verdict.jarvondis_score,
                    "krystal": guardian_verdict.krystal_score,
                    "miko": guardian_verdict.miko_score,
                    "reason": guardian_verdict.rejection_reason,
                },
            )

            return ExecutionReceipt(
                intent_id=packet.intent_id,
                status="REJECTED",
                evidence_hash=evidence_record.record_hash,
                result={
                    "error": guardian_verdict.rejection_reason,
                    "scores": {
                        "jarvondis": guardian_verdict.jarvondis_score,
                        "krystal": guardian_verdict.krystal_score,
                        "miko": guardian_verdict.miko_score,
                    },
                },
            )

        # Stage 3: Governance Verification
        governance_result = self.governance.evaluate_intent(packet)
        if not governance_result.passed:
            # Log governance rejection
            evidence_record = self.governance.evidence_ledger.append(
                event_type="GOVERNANCE_REJECTED",
                actor_id=packet.caller_id,
                intent_id=packet.intent_id,
                payload={
                    "action": packet.action,
                    "reason": governance_result.rejection_reason,
                },
            )

            return ExecutionReceipt(
                intent_id=packet.intent_id,
                status="REJECTED",
                evidence_hash=evidence_record.record_hash,
                result={"error": governance_result.rejection_reason},
            )

        # Stage 4: Log Approved Intent to Evidence Ledger
        evidence_record = self.governance.evidence_ledger.append(
            event_type="GOVERNANCE_APPROVED",
            actor_id=packet.caller_id,
            intent_id=packet.intent_id,
            payload={
                "action": packet.action,
                "guardian_scores": {
                    "jarvondis": guardian_verdict.jarvondis_score,
                    "krystal": guardian_verdict.krystal_score,
                    "miko": guardian_verdict.miko_score,
                },
            },
        )

        # Stage 5: Dispatch to Arach for Execution
        try:
            arach_result = self.arach.dispatch(
                intent_id=packet.intent_id,
                caller_id=packet.caller_id,
                action=packet.action,
                payload=packet.payload,
            )
        except Exception as e:
            # Log execution failure
            self.governance.evidence_ledger.append(
                event_type="TASK_FAILED",
                actor_id=packet.caller_id,
                intent_id=packet.intent_id,
                payload={"error": str(e)},
            )
            return ExecutionReceipt(
                intent_id=packet.intent_id,
                status="REJECTED",
                evidence_hash=evidence_record.record_hash,
                result={"error": f"Execution failed: {str(e)}"},
            )

        # Stage 6: Log Successful Execution
        final_evidence = self.governance.evidence_ledger.append(
            event_type="TASK_COMPLETED",
            actor_id=packet.caller_id,
            intent_id=packet.intent_id,
            payload={"result_hash": hash(str(arach_result))},
        )

        # Return Governed Execution Receipt
        receipt = ExecutionReceipt(
            intent_id=packet.intent_id,
            status="SUCCESS",
            evidence_hash=final_evidence.record_hash,
            result=arach_result,
        )

        self.execution_log.append(
            {
                "intent_id": packet.intent_id,
                "status": receipt.status,
                "timestamp": receipt.timestamp,
            }
        )

        return receipt

    def get_execution_log(self) -> list:
        """Retrieve log of all executions."""
        return self.execution_log
