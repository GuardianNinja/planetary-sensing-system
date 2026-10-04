"""
Arach Task Web
Tasks are silk threads woven into a living web of dependencies.

Blueprint anchor:
"Tasks are silk threads — priority shown by thread thickness (1 = gossamer, 5 = anchor silk)."
"""

from enum import Enum
from dataclasses import dataclass, field
import time


class PulseState(Enum):
    NORMAL = "NORMAL"
    GENTLE_PULSE = "GENTLE_PULSE"  # overdue but non‑shaming
    ATTENTION = "ATTENTION"        # user‑requested focus


@dataclass
class SilkThread:
    task_id: str
    title: str
    thickness: int  # 1–5
    dependencies: list[str]
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    pulse: PulseState = PulseState.NORMAL

    def mark_updated(self):
        self.updated_at = time.time()

    def set_pulse(self, state: PulseState):
        self.pulse = state

    def add_dependency(self, dep_id: str):
        if dep_id not in self.dependencies:
            self.dependencies.append(dep_id)

    def remove_dependency(self, dep_id: str):
        if dep_id in self.dependencies:
            self.dependencies.remove(dep_id)


class TaskWeb:
    def __init__(self):
        self.threads: dict[str, SilkThread] = {}

    def add_thread(self, thread: SilkThread):
        self.threads[thread.task_id] = thread

    def get_thread(self, task_id: str) -> SilkThread | None:
        return self.threads.get(task_id)

    def overdue_pulse_scan(self, threshold_days: int = 3):
        """Soft pulse for overdue tasks — no alarm, no shame."""
        now = time.time()
        for thread in self.threads.values():
            age_days = (now - thread.updated_at) / 86400
            if age_days >= threshold_days:
                thread.set_pulse(PulseState.GENTLE_PULSE)
