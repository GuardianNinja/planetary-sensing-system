from user_worlds.arach_adapter import ArachAdapter, UserIdentity, EvidenceCache
from task_spider.arach.arach_dispatcher import ArachDispatcher

def build_kernel_for_world(world_id: str, display_name: str) -> HIKernelOrchestrator:
    identity = UserIdentity(
        user_id=world_id,
        lineage_key="LOCAL-ONLY",  # placeholder until full identity spine
        display_name=display_name,
    )
    evidence_cache = EvidenceCache()
    adapter = ArachAdapter(identity=identity, evidence_cache=evidence_cache)
    dispatcher = ArachDispatcher(adapter=adapter)
    governance = GovernanceEnforcer(min_guardian_threshold=0.85)

    return HIKernelOrchestrator(governance=governance, arach_dispatcher=dispatcher)
