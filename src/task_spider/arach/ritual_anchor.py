"""
Arach Ritual Anchor
Manages daily, weekly, and monthly ceremonies.

Blueprint anchor:
"Manages daily routines, morning rituals, evening wind-downs, weekly reviews, and monthly checkpoints."
"""

from dataclasses import dataclass, field
import time


@dataclass
class Ritual:
    ritual_id: str
    name: str
    cadence: str  # daily, weekly, monthly, ceremonial
    last_completed: float = field(default_factory=lambda: 0.0)
    prompts: list[str] = field(default_factory=list)

    def complete(self):
        self.last_completed = time.time()

    def add_prompt(self, prompt: str):
        self.prompts.append(prompt)


class RitualAnchor:
    def __init__(self):
        self.rituals: dict[str, Ritual] = {}

    def add_ritual(self, ritual: Ritual):
        self.rituals[ritual.ritual_id] = ritual

    def get_due_rituals(self) -> list[Ritual]:
        """Return rituals due based on cadence."""
        now = time.time()
        due = []

        for ritual in self.rituals.values():
            delta = now - ritual.last_completed

            if ritual.cadence == "daily" and delta > 86400:
                due.append(ritual)
            elif ritual.cadence == "weekly" and delta > 604800:
                due.append(ritual)
            elif ritual.cadence == "monthly" and delta > 2592000:
                due.append(ritual)

        return due

    def captain_log_prompt(self) -> str:
        """Generate a Captain’s Log prompt."""
        return "Captain, record today’s witness entry."
