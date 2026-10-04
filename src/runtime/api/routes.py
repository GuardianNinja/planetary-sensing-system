# src/runtime/api/routes.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi import status as http_status

from src.runtime.user_world_context import UserWorldContext, get_user_world_context
from src.hi_kernel.intent_interpreter import IntentInterpreter
from src.hi_kernel.guardian_interceptor import GuardianInterceptor
from src.governance.governance_enforcer import GovernanceEnforcer
from src.governance.evidence_ledger import EvidenceLedgerService
from src.task_spider.arach_dispatcher import ArachDispatcher
from src.hi_kernel.orchestrator import HIOrchestrator
from src.hi_kernel.recombination_layer import RecombinationLayer
from src.runtime.models import IntentRequest, IntentReceipt


def register_intent_routes(app: FastAPI) -> None:
    @app.post("/v1/intent", response_model=IntentReceipt)
    async def handle_intent(
        payload: IntentRequest,
        world_ctx: UserWorldContext = Depends(get_user_world_context),
    ) -> IntentReceipt:
        # 1) Gateway validates JSON shape via Pydantic (IntentRequest)
        # 2) IntentInterpreter normalizes intent
        interpreter = IntentInterpreter(world_ctx)
        normalized_intent = interpreter.normalize(payload)

        # 3) GuardianInterceptor evaluates J/K/M (jurisdiction, kernel, mode)
        guardian = GuardianInterceptor(world_ctx)
        guardian_decision = guardian.evaluate(normalized_intent)
        if not guardian_decision.allowed:
            return IntentReceipt(
                intent_id=normalized_intent.intent_id,
                status="REJECTED",
                evidence_hash=None,
                result={"reason": "GuardianInterceptor rejected intent"},
            )

        # 4) GovernanceEnforcer checks identity, lane, safety
        enforcer = GovernanceEnforcer(world_ctx)
        if not enforcer.authorize(normalized_intent):
            return IntentReceipt(
                intent_id=normalized_intent.intent_id,
                status="REJECTED",
                evidence_hash=None,
                result={"reason": "GovernanceEnforcer denied authorization"},
            )

        # 5) EvidenceLedgerService appends signed hash entry before execution
        ledger = EvidenceLedgerService(world_ctx)
        evidence_hash = ledger.commit_pre_execution(normalized_intent)

        if evidence_hash is None:
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ledger commitment failed; execution aborted.",
            )

        # 6) ArachDispatcher creates task thread + cocoon + local execution
        dispatcher = ArachDispatcher(world_ctx)
        task_result = await dispatcher.execute_intent(normalized_intent)

        # 7) HI orchestrator recombines results
        orchestrator = HIOrchestrator(world_ctx)
        recombiner = RecombinationLayer()
        recombined = orchestrator.recombine(task_result, recombiner)

        # 8) Final receipt
        return IntentReceipt(
            intent_id=normalized_intent.intent_id,
            status="SUCCESS",
            evidence_hash=evidence_hash,
            result=recombined,
        )
