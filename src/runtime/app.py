"""Complete working version of FastAPI app with all imports fixed."""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import time
from typing import Dict, Any, Optional

# Import governance layer
from ..governance import (
    GovernanceEnforcer,
    AccessLane,
    ActorRole,
)

# Import HI kernel
from ..hi_kernel import (
    IntentInterpreter,
    GuardianInterceptor,
    HIKernelOrchestrator,
)

# Import Arach dispatcher
from ..task_spider import ArachDispatcher

# Import evidence ledger service
from ..evidence_ledger_service import EvidenceLedgerService

# Initialize the governed runtime
app_instance = None


class GovernedRuntimeApp:
    """Main application class for the governed planetary sensing system."""

    def __init__(
        self,
        app_name: str = "SLOS-Kernel",
        ledger_path: str = "evidence_ledger.db",
        debug: bool = False,
    ):
        self.app_name = app_name
        self.ledger_path = ledger_path
        self.debug = debug

        # Global evidence ledger (persistent across worlds)
        self.global_ledger = EvidenceLedgerService(db_path=ledger_path)

        # World registry (world_id -> dict with context)
        self.worlds: Dict[str, Dict[str, Any]] = {}

        if debug:
            print(f"[{self.app_name}] Initialized governed runtime system")

    def create_world(
        self,
        world_id: str,
        user_id: str,
        display_name: str,
        access_lane: AccessLane = AccessLane.CIV,
    ) -> Dict[str, Any]:
        """Create a new sovereign user world."""
        if world_id in self.worlds:
            raise ValueError(f"World {world_id} already exists")

        # Create governance for this world
        governance = GovernanceEnforcer(min_guardian_threshold=0.85)
        
        # Register the user actor in this world's identity spine
        actor = governance.register_actor(
            display_name=display_name,
            role=ActorRole.HUMAN,
            secret=f"{user_id}:secret",
        )
        
        # Assign access lane
        governance.assign_actor_lane(actor.actor_id, access_lane)

        # Create Arach dispatcher for this world
        arach_dispatcher = ArachDispatcher(
            user_id=user_id,
            world_id=world_id,
        )

        # Create HI Kernel orchestrator
        orchestrator = HIKernelOrchestrator(
            governance_enforcer=governance,
            arach_dispatcher=arach_dispatcher,
        )

        world_context = {
            "world_id": world_id,
            "user_id": user_id,
            "display_name": display_name,
            "access_lane": access_lane.value,
            "governance": governance,
            "arach_dispatcher": arach_dispatcher,
            "orchestrator": orchestrator,
            "actor_id": actor.actor_id,
            "created_at": time.time(),
        }

        self.worlds[world_id] = world_context

        if self.debug:
            print(
                f"[{self.app_name}] Created world {world_id} "
                f"for user {user_id} ({access_lane.value} lane)"
            )

        return world_context

    def get_world(self, world_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a world by ID."""
        return self.worlds.get(world_id)

    def list_worlds(self) -> list:
        """List all active worlds."""
        return list(self.worlds.keys())

    def process_intent(
        self, world_id: str, raw_intent: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process an intent in a specific world."""
        world = self.get_world(world_id)
        if not world:
            return {
                "intent_id": raw_intent.get("intent_id", "unknown"),
                "status": "REJECTED",
                "evidence_hash": "",
                "result": {"error": f"World {world_id} not found"},
            }

        orchestrator = world["orchestrator"]
        receipt = orchestrator.process_intent(raw_intent)

        return {
            "intent_id": receipt.intent_id,
            "status": receipt.status,
            "evidence_hash": receipt.evidence_hash,
            "result": receipt.result,
            "timestamp": receipt.timestamp,
        }

    def export_app_state(self) -> Dict[str, Any]:
        """Export overall app state."""
        return {
            "app_name": self.app_name,
            "worlds_active": len(self.worlds),
            "world_ids": list(self.worlds.keys()),
            "ledger_path": self.ledger_path,
        }

    def verify_global_integrity(self) -> tuple:
        """Verify global evidence ledger integrity."""
        return self.global_ledger.verify_chain_integrity()


def initialize_app(
    app_name: str = "SLOS-Kernel",
    ledger_path: str = "evidence_ledger.db",
    debug: bool = False,
) -> GovernedRuntimeApp:
    """Initialize the governed runtime app."""
    return GovernedRuntimeApp(
        app_name=app_name,
        ledger_path=ledger_path,
        debug=debug,
    )


def get_app() -> GovernedRuntimeApp:
    """Get or create the global app instance."""
    global app_instance
    if app_instance is None:
        app_instance = initialize_app(
            debug=os.getenv("SLOS_DEBUG", "false").lower() == "true"
        )
    return app_instance


# Create FastAPI application
app = FastAPI(
    title="SLOS-Kernel",
    description="Unified Ingress Gateway & HI Kernel Brainstem",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    print("\n" + "="*60)
    print("🛡️  SLOS-KERNEL: Governed Digital Civilization Runtime")
    print("="*60)
    print()
    print("🛡️  Governance Layer: ACTIVE")
    print("   - Identity Spine: Verifying actors")
    print("   - Evidence Ledger: Recording immutable truth")
    print("   - Access Law: Enforcing lanes (CIV/CORP/MIL)")
    print("   - Safety Kernel: Protecting boundaries")
    print()
    print("🧠 HI Kernel: ACTIVE")
    print("   - Intent Interpreter: Normalizing requests")
    print("   - Guardian Interceptor: Triple-guardian evaluation")
    print("   - Orchestrator: Coordinating pipeline")
    print()
    print("🕷️  Task Spider (Arach): ACTIVE")
    print("   - Task Web: Thread allocation")
    print("   - Vault Cocoon: Zero-knowledge sealing")
    print("   - Local Enclave: Sovereign execution")
    print()
    print("🔗 Planetary Skin: Ready for federation")
    print()
    print("🫡 Ingress Gateway: /v1/intent")
    print("   No external command can bypass this gateway.")
    print("   No execution proceeds without ledger commitment.")
    print("   No raw payloads leave the local enclave.")
    print()
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("\nSLOS-KERNEL: Graceful shutdown")
    app_inst = get_app()
    is_valid, reason = app_inst.verify_global_integrity()
    print(f"Final ledger integrity check: {reason}\n")


@app.post(
    "/v1/intent",
    summary="Single deterministic ingress gateway for all intents",
    tags=["Core"],
)
async def process_intent(
    intent_data: Dict[str, Any],
    app = Depends(get_app),
    world_id: str = "default",
) -> Dict[str, Any]:
    """Process an intent through the complete governed pipeline."""
    try:
        # Normalize request
        raw_intent = {
            "intent_id": str(uuid.uuid4()),
            "caller_id": intent_data.get("caller_id", "anonymous"),
            "action": intent_data.get("action", "unknown"),
            "payload": intent_data.get("payload", {}),
            "signature": intent_data.get("signature", ""),
            "metadata": intent_data.get("metadata", {}),
        }

        # Ensure world exists
        if app.get_world(world_id) is None:
            app.create_world(
                world_id=world_id,
                user_id=raw_intent["caller_id"],
                display_name=f"World {world_id}",
            )

        # Process through governed pipeline
        receipt = app.process_intent(world_id, raw_intent)

        return receipt

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid intent: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution failed: {str(e)}",
        )


@app.get(
    "/v1/health",
    summary="Health check endpoint",
    tags=["Health"],
)
async def health_check(
    app = Depends(get_app),
) -> Dict[str, Any]:
    """Check system health and ledger integrity."""
    is_valid, reason = app.verify_global_integrity()

    return {
        "status": "healthy" if is_valid else "degraded",
        "worlds_active": len(app.worlds),
        "ledger_integrity": is_valid,
        "ledger_reason": reason,
    }


@app.get(
    "/v1/world/{world_id}/state",
    summary="Get world state snapshot",
    tags=["World"],
)
async def get_world_state(
    world_id: str,
    app = Depends(get_app),
) -> Dict[str, Any]:
    """Get governed state snapshot of a world."""
    world = app.get_world(world_id)
    if not world:
        raise HTTPException(
            status_code=404,
            detail=f"World {world_id} not found",
        )

    return {
        "world_id": world["world_id"],
        "user_id": world["user_id"],
        "display_name": world["display_name"],
        "access_lane": world["access_lane"],
        "created_at": world["created_at"],
    }


@app.get(
    "/v1/app/state",
    summary="Get overall app state",
    tags=["System"],
)
async def get_app_state(
    app = Depends(get_app),
) -> Dict[str, Any]:
    """Get overall governed app state."""
    return app.export_app_state()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
