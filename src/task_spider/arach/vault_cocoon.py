"""
Arach Vault Cocoon
Local‑first encrypted bundles for documents, notes, ideas, and reference items.

Cocoons follow the blueprint principle:
"Organized in cocoons — each one a self-contained, encrypted bundle."
"""

from enum import Enum
from dataclasses import dataclass, field
import time
import hashlib
import json


class PrivacyLevel(Enum):
    PRIVATE = "PRIVATE"
    SHARED = "SHARED"
    CEREMONIAL = "CEREMONIAL"


@dataclass
class Cocoon:
    cocoon_id: str
    payload: dict
    tags: list[str]
    privacy: PrivacyLevel
    created_at: float = field(default_factory=time.time)
    checksum: str = field(init=False)

    def __post_init__(self):
        self.checksum = self._generate_checksum()

    def _generate_checksum(self) -> str:
        raw = json.dumps(self.payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def verify_integrity(self) -> bool:
        """Validate checksum and ensure payload has not been tampered."""
        return self.checksum == self._generate_checksum()

    def update_payload(self, new_payload: dict):
        """Update payload and regenerate checksum."""
        self.payload = new_payload
        self.checksum = self._generate_checksum()

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)
