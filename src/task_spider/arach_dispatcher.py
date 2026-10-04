"""Arach Dispatcher — Task execution engine for the User World enclave.

The Arach Dispatcher routes approved tasks into the local user world,
executes them within a sovereign enclave boundary, and returns
zero-knowledge validated results.

Blueprint anchor:
"Arach Local Execution (User World Enclave).
Leg 1: Task Web Thread Allocation
Leg 2: Zero-Knowledge Vault Sealing
Leg 3: Local User World Enclave Execution"
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid
import time

from .arach.task_web import TaskWeb, SilkThread, PulseState
from .arach.vault_cocoon import VaultCocoon, Cocoon, PrivacyLevel
from .arach.alert_sense import AlertSense, Sensitivity
from .arach.ritual_anchor import RitualAnchor


@dataclass
class DispatchRequest:
    """Request to dispatch a task into Arach."""
    intent_id: str
    caller_id: str
    action: str
    payload: Dict[str, Any]
    evidence_hash: str


@dataclass
class DispatchResult:
    """Result of Arach execution."""
    intent_id: str
    success: bool
    task_id: str
    cocoon_id: str  # Zero-knowledge sealed container
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class ArachDispatcher:
    """Executes tasks within sovereign user-world enclave."""

    def __init__(self, user_id: str, world_id: str):
        self.user_id = user_id
        self.world_id = world_id
        self.task_web = TaskWeb()
        self.vault = VaultCocoon()
        self.alert_sense = AlertSense(Sensitivity.GENTLE_HUM)
        self.ritual_anchor = RitualAnchor()
        self.dispatch_log = []

    def dispatch(
        self,
        intent_id: str,
        caller_id: str,
        action: str,
        payload: Dict[str, Any],
        evidence_hash: str = "",
    ) -> Dict[str, Any]:
        """Execute a task within the user-world enclave.

        Three legs of execution:
        1. Task Web: Create/update SilkThread for this task
        2. Vault: Seal payload in zero-knowledge cocoon
        3. Execute: Run action within sovereign boundary

        Returns zero-knowledge validated result (never exposes raw payload).
        """

        try:
            # Leg 1: Task Web Thread Allocation
            task_id = str(uuid.uuid4())
            thickness = self._calculate_priority(action)
            thread = SilkThread(
                task_id=task_id,
                title=f"{action} @ {self.world_id}",
                thickness=thickness,
                dependencies=[],
            )
            self.task_web.add_thread(thread)

            # Leg 2: Zero-Knowledge Vault Sealing
            cocoon_id = str(uuid.uuid4())
            cocoon = self.vault.create_cocoon(
                cocoon_id=cocoon_id,
                payload=payload,
                tags=[action, self.world_id, caller_id],
                privacy=PrivacyLevel.PRIVATE,
            )

            # Leg 3: Local User World Enclave Execution
            execution_result = self._execute_in_enclave(
                task_id=task_id,
                action=action,
                cocoon_id=cocoon_id,
                payload=payload,
            )

            # Mark thread as completed
            thread.mark_updated()
            thread.set_pulse(PulseState.NORMAL)

            # Log dispatch
            dispatch_result = DispatchResult(
                intent_id=intent_id,
                success=True,
                task_id=task_id,
                cocoon_id=cocoon_id,
                metadata={
                    "world_id": self.world_id,
                    "caller_id": caller_id,
                    "action": action,
                    "evidence_hash": evidence_hash,
                    "thread_thickness": thickness,
                },
            )

            self.dispatch_log.append(
                {
                    "intent_id": intent_id,
                    "task_id": task_id,
                    "status": "SUCCESS",
                    "timestamp": time.time(),
                }
            )

            # Return zero-knowledge result (cocoon reference only, not payload)
            return {
                "intent_id": intent_id,
                "task_id": task_id,
                "cocoon_id": cocoon_id,
                "status": "SUCCESS",
                "result": execution_result,
                "metadata": dispatch_result.metadata,
            }

        except Exception as e:
            self.dispatch_log.append(
                {
                    "intent_id": intent_id,
                    "status": "FAILED",
                    "error": str(e),
                    "timestamp": time.time(),
                }
            )
            raise

    def _calculate_priority(self, action: str) -> int:
        """Calculate thread thickness (priority) based on action.

        Priority scale:
        1 = gossamer (low)
        2 = light
        3 = medium
        4 = strong
        5 = anchor silk (critical)
        """
        priority_map = {
            "verify": 5,
            "audit": 5,
            "governance": 4,
            "identity": 4,
            "create": 3,
            "update": 2,
            "read": 1,
        }
        for key, value in priority_map.items():
            if key in action.lower():
                return value
        return 2  # Default: light

    def _execute_in_enclave(
        self,
        task_id: str,
        action: str,
        cocoon_id: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute action within sovereign user-world boundary.

        This is where the actual task logic happens.
        The enclave is isolated from other worlds.
        """

        # Route to action handler
        if action == "create_task":
            return self._handle_create_task(payload)
        elif action == "read_task":
            return self._handle_read_task(payload)
        elif action == "update_task":
            return self._handle_update_task(payload)
        elif action == "list_tasks":
            return self._handle_list_tasks(payload)
        elif action == "create_ritual":
            return self._handle_create_ritual(payload)
        else:
            # Generic execution: log and return metadata
            return {
                "action": action,
                "status": "executed",
                "cocoon_id": cocoon_id,
                "timestamp": time.time(),
            }

    def _handle_create_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_task action within enclave."""
        title = payload.get("title", "Untitled")
        thickness = payload.get("thickness", 2)
        thread = SilkThread(
            task_id=str(uuid.uuid4()),
            title=title,
            thickness=thickness,
            dependencies=payload.get("dependencies", []),
        )
        self.task_web.add_thread(thread)
        return {
            "task_id": thread.task_id,
            "title": thread.title,
            "created_at": thread.created_at,
        }

    def _handle_read_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle read_task action within enclave."""
        task_id = payload.get("task_id")
        thread = self.task_web.get_thread(task_id)
        if not thread:
            return {"error": f"Task {task_id} not found"}
        return {
            "task_id": thread.task_id,
            "title": thread.title,
            "thickness": thread.thickness,
            "pulse": thread.pulse.value,
        }

    def _handle_update_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_task action within enclave."""
        task_id = payload.get("task_id")
        thread = self.task_web.get_thread(task_id)
        if not thread:
            return {"error": f"Task {task_id} not found"}
        thread.mark_updated()
        return {"task_id": thread.task_id, "updated_at": thread.updated_at}

    def _handle_list_tasks(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_tasks action within enclave."""
        tasks = [
            {
                "task_id": t.task_id,
                "title": t.title,
                "thickness": t.thickness,
            }
            for t in self.task_web.threads.values()
        ]
        return {"tasks": tasks, "count": len(tasks)}

    def _handle_create_ritual(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_ritual action within enclave."""
        from .arach.ritual_anchor import Ritual

        ritual = Ritual(
            ritual_id=str(uuid.uuid4()),
            name=payload.get("name", "Unnamed Ritual"),
            cadence=payload.get("cadence", "daily"),
            prompts=payload.get("prompts", []),
        )
        self.ritual_anchor.add_ritual(ritual)
        return {
            "ritual_id": ritual.ritual_id,
            "name": ritual.name,
            "cadence": ritual.cadence,
        }

    def get_dispatch_log(self) -> list:
        """Retrieve log of all dispatches."""
        return self.dispatch_log

    def export_safe_state(self) -> Dict[str, Any]:
        """Export governed, privacy-preserving state snapshot.

        Never exposes raw payloads or private data.
        Only metadata and indices.
        """
        return {
            "world_id": self.world_id,
            "user_id": self.user_id,
            "task_count": len(self.task_web.threads),
            "vault_index": list(self.vault.cocoons.keys()),
            "rituals": list(self.ritual_anchor.rituals.keys()),
        }
