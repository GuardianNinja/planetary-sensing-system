"""
Arach Adapter — Sovereign User World Mount

This module binds a local Arach instance into a specific User World.
It provides:

• Local identity domain access
• Evidence cache binding
• Safe, governed APIs exposed to the global Task Spider

Blueprint anchors:
"Each human receives a fully sovereign digital world."
"Local agents + local spider."
"""

from dataclasses import dataclass
from typing import Optional

# Local Arach modules
from task_spider.arach.vault_cocoon import Cocoon, PrivacyLevel
from task_spider.arach.task_web import TaskWeb, SilkThread
from task_spider.arach.alert_sense import AlertSense, Sensitivity
from task_spider.arach.ritual_anchor import RitualAnchor, Ritual


@dataclass
class UserIdentity:
    user_id: str
    lineage_key: str
    display_name: str


class EvidenceCache:
    """
    Local evidence cache inside the User World.
    Stores governed truth artifacts, cocoon references, and task logs.
    """
    def __init__(self):
        self.records = {}

    def store(self, key: str, value: dict):
        self.records[key] = value

    def fetch(self, key: str) -> Optional[dict]:
        return self.records.get(key)


class ArachAdapter:
    """
    Adapter that mounts Arach inside a sovereign User World.

    Responsibilities:
    • Read local identity
    • Bind to evidence cache
    • Expose safe APIs to global Task Spider
    """

    def __init__(self, identity: UserIdentity, evidence_cache: EvidenceCache):
        self.identity = identity
        self.evidence_cache = evidence_cache

        # Local Arach subsystems
        self.task_web = TaskWeb()
        self.vault = {}
        self.alert_sense = AlertSense(Sensitivity.GENTLE_HUM)
        self.ritual_anchor = RitualAnchor()

    # ---------------------------------------------------------
    # Identity & Evidence Cache
    # ---------------------------------------------------------

    def get_identity(self) -> UserIdentity:
        """Return the sovereign identity domain for this User World."""
        return self.identity

    def log_evidence(self, key: str, value: dict):
        """Store governed evidence into the local cache."""
        self.evidence_cache.store(key, value)

    # ---------------------------------------------------------
    # Vault Cocoon APIs
    # ---------------------------------------------------------

    def create_cocoon(self, cocoon_id: str, payload: dict, tags: list[str],
                      privacy: PrivacyLevel = PrivacyLevel.PRIVATE):
        cocoon = Cocoon(cocoon_id=cocoon_id, payload=payload, tags=tags, privacy=privacy)
        self.vault[cocoon_id] = cocoon
        return cocoon

    def get_cocoon(self, cocoon_id: str) -> Optional[Cocoon]:
        return self.vault.get(cocoon_id)

    # ---------------------------------------------------------
    # Task Web APIs (safe for global Task Spider)
    # ---------------------------------------------------------

    def add_task(self, task_id: str, title: str, thickness: int, dependencies: list[str]):
        thread = SilkThread(
            task_id=task_id,
            title=title,
            thickness=thickness,
            dependencies=dependencies,
        )
        self.task_web.add_thread(thread)
        return thread

    def get_task(self, task_id: str) -> Optional[SilkThread]:
        return self.task_web.get_thread(task_id)

    def pulse_scan(self):
        """Run gentle overdue pulse scan."""
        self.task_web.overdue_pulse_scan()

    # ---------------------------------------------------------
    # Alert Sense APIs
    # ---------------------------------------------------------

    def notify(self, message: str):
        """Send a gentle Spider Sense alert."""
        return self.alert_sense.notify(message)

    # ---------------------------------------------------------
    # Ritual Anchor APIs
    # ---------------------------------------------------------

    def add_ritual(self, ritual_id: str, name: str, cadence: str, prompts: list[str]):
        ritual = Ritual(
            ritual_id=ritual_id,
            name=name,
            cadence=cadence,
            prompts=prompts,
        )
        self.ritual_anchor.add_ritual(ritual)
        return ritual

    def due_rituals(self):
        return self.ritual_anchor.get_due_rituals()

    def captain_log_prompt(self):
        return self.ritual_anchor.captain_log_prompt()

    # ---------------------------------------------------------
    # Global Task Spider Safe API Surface
    # ---------------------------------------------------------

    def export_safe_state(self) -> dict:
        """
        Export a governed, privacy‑preserving snapshot for the global Task Spider.
        No private cocoon payloads, no raw identity secrets.
        """

        return {
            "user_id": self.identity.user_id,
            "task_count": len(self.task_web.threads),
            "vault_index": list(self.vault.keys()),
            "rituals": list(self.ritual_anchor.rituals.keys()),
            "alert_mode": self.alert_sense.sensitivity.value,
        }
