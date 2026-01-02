
"""
Captain's Secure Link Module v0.1
Reference implementation for:
- SecureMessage format
- Signing and verification
- Basic routing policy abstraction
"""
"""
Captain's Secure Link Module v0.1
Reference implementation for:
- SecureMessage format
- Signing and verification
- Basic routing policy abstraction
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
# -----------------------
# Authorization
# -----------------------

class AuthorizedMembers:
    """
    Manages the set of authorized member IDs.
    """
    def __init__(self, members: Optional[set[str]] = None):
        self.members = members or set()

    def is_authorized(self, member_id: str) -> bool:
        return member_id in self.members

    def add_member(self, member_id: str):
        self.members.add(member_id)

    def remove_member(self, member_id: str):
        self.members.discard(member_id)
import json
import time
import hmac
import hashlib


# -----------------------
# Priority and message
# -----------------------

class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class SecureMessage:
    sender_id: str
    recipient_id: str
    priority: Priority
    timestamp: int
    ttl: int
    payload: str
    nonce: str
    signature: str = ""



def sign_message(secret_key: bytes, msg: SecureMessage, authorized: AuthorizedMembers) -> SecureMessage:
    if not authorized.is_authorized(msg.sender_id):
        raise PermissionError("Sender is not authorized")
    if not authorized.is_authorized(msg.recipient_id):
        raise PermissionError("Recipient is not authorized")
    body: dict[str, object] = {
        "sender_id": msg.sender_id,
        "recipient_id": msg.recipient_id,
        "priority": msg.priority.value,
        "timestamp": msg.timestamp,
        "ttl": msg.ttl,
        "payload": msg.payload,
        "nonce": msg.nonce,
    }
    encoded = json.dumps(body, sort_keys=True).encode("utf-8")
    sig = hmac.new(secret_key, encoded, hashlib.sha256).hexdigest()
    msg.signature = sig
    return msg



def verify_message(
    secret_key: bytes,
    msg: SecureMessage,
    authorized: AuthorizedMembers,
    replay_window_seconds: int = 300,
    seen_nonces: Optional[set[str]] = None,
) -> bool:
    if not authorized.is_authorized(msg.sender_id):
        return False
    if not authorized.is_authorized(msg.recipient_id):
        return False
    if seen_nonces is None:
        seen_nonces = set()

    now = int(time.time())
    if now > msg.timestamp + msg.ttl:
        return False

    if msg.nonce in seen_nonces:
        return False

    body: dict[str, object] = {
        "sender_id": msg.sender_id,
        "recipient_id": msg.recipient_id,
        "priority": msg.priority.value,
        "timestamp": msg.timestamp,
        "ttl": msg.ttl,
        "payload": msg.payload,
        "nonce": msg.nonce,
    }
    encoded: bytes = json.dumps(body, sort_keys=True).encode("utf-8")
    expected_sig = hmac.new(secret_key, encoded, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_sig, msg.signature):
        return False

    seen_nonces.add(msg.nonce)
    return True


# -----------------------
# Routing policy
# -----------------------

class LinkType(Enum):
    DIRECT_CELL = "direct_cell"
    SECURE_DEVICE = "secure_device"
    SATELLITE = "satellite"


@dataclass
class RoutePolicy:
    link_preference: List[LinkType]
    require_secure_device: bool
    allowed_endpoints: List[str]



class SecureRouter:
    def __init__(self, policy: RoutePolicy, authorized: AuthorizedMembers):
        self.policy = policy
        self.authorized = authorized

    def select_link(self, available_links: List[LinkType]) -> Optional[LinkType]:
        """
        Select the best link based on policy and current availability.
        """
        if self.policy.require_secure_device and LinkType.SECURE_DEVICE not in available_links:
            return None

        for pref in self.policy.link_preference:
            if pref in available_links:
                return pref

        return None

    def send(self, destination: str, data: bytes, available_links: List[LinkType]) -> bool:
        if not self.authorized.is_authorized(destination):
            raise PermissionError("Destination not authorized as member")
        if destination not in self.policy.allowed_endpoints:
            raise PermissionError("Destination not allowed by policy")

        link = self.select_link(available_links)
        if link is None:
            return False

        if link == LinkType.SECURE_DEVICE:
            self._send_to_secure_device(destination, data)
        elif link == LinkType.SATELLITE:
            self._send_via_satellite(destination, data)
        else:
            self._send_direct(destination, data)

        return True

    # Placeholder methods to be implemented per platform/hardware:

    def _send_to_secure_device(self, destination: str, data: bytes):
        # Implement USB/BLE communication with hardware node
        pass

    def _send_via_satellite(self, destination: str, data: bytes):
        # Implement satellite modem integration
        pass

    def _send_direct(self, destination: str, data: bytes):
        # Implement direct TLS/HTTPS from host device
        pass
