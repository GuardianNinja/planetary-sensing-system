# src/governance/governance_enforcer.py
from src.runtime.models import NormalizedIntent
from src.runtime.user_world_context import UserWorldContext
from .identity_spine import IdentitySpine
from .access_law import AccessLaw
from .safety_kernel import SafetyKernel

class GovernanceEnforcer:
    def __init__(self, world_ctx: UserWorldContext):
        self.world_ctx = world_ctx
        self.identity_spine = IdentitySpine(world_ctx.identity)
        self.access_law = AccessLaw(world_ctx.lane, world_ctx.safety_profile)
        self.safety_kernel = SafetyKernel(world_ctx.safety_profile)

    def authorize(self, intent: NormalizedIntent) -> bool:
        subject = self.identity_spine.resolve_subject()
        lanes = self.identity_spine.resolve_lanes()
        # Use subject + lanes + safety to decide
        allowed = self.access_law.can_execute_intent(intent.intent_type, intent.payload)
        if not allowed:
            return False

        # Sanitize payload before leaving governance boundary
        intent.payload = self.safety_kernel.sanitize_payload(intent.payload)
        return True
