"""
Arach Dispatcher — bridge between HI Kernel and local ArachAdapter.
"""

from typing import Any, Dict
from user_worlds.arach_adapter import ArachAdapter


class ArachDispatcher:
    def __init__(self, adapter: ArachAdapter):
        self.adapter = adapter

    def dispatch(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map high-level actions into ArachAdapter operations.
        This is the only surface the HI Kernel talks to.
        """
        if action == "add_task":
            thread = self.adapter.add_task(
                task_id=payload["task_id"],
                title=payload["title"],
                thickness=payload.get("thickness", 3),
                dependencies=payload.get("dependencies", []),
            )
            return {"status": "TASK_ADDED", "task_id": thread.task_id}

        if action == "create_cocoon":
            cocoon = self.adapter.create_cocoon(
                cocoon_id=payload["cocoon_id"],
                payload=payload["data"],
                tags=payload.get("tags", []),
            )
            return {"status": "COCOON_CREATED", "cocoon_id": cocoon.cocoon_id}

        if action == "pulse_scan":
            self.adapter.pulse_scan()
            return {"status": "PULSE_SCAN_COMPLETE"}

        # Default: unknown action
        return {"status": "UNKNOWN_ACTION", "action": action}
