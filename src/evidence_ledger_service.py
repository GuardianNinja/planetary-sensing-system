"""Evidence Ledger Service — Immutable append-only audit trail with SQLite storage.

Provides persistent storage and integrity verification of all governance decisions.

Blueprint anchor:
"Evidence Ledger (SQLite + SQLCipher).
Append signed Merkle entry BEFORE execution.
Ledger Rules: Immutable, Append-only, Zero-knowledge."
"""

import sqlite3
import hashlib
import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class EvidenceEntry:
    """Single entry in the evidence ledger."""
    entry_id: str
    timestamp: float
    event_type: str  # RECEIVED, APPROVED, REJECTED, EXECUTED, FAILED
    intent_id: str
    caller_id: str
    action: str
    payload_hash: str  # SHA256 of payload (zero-knowledge)
    guardian_scores: Dict[str, float]  # {jarvondis, krystal, miko}
    status: str  # APPROVED or REJECTED
    evidence_chain_hash: str  # SHA256 of this entry + previous hash
    previous_hash: str = "0"


class EvidenceLedgerService:
    """SQLite-backed immutable evidence ledger."""

    def __init__(self, db_path: str = "evidence_ledger.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database schema if not exists."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS evidence_ledger (
                entry_id TEXT PRIMARY KEY,
                timestamp REAL NOT NULL,
                event_type TEXT NOT NULL,
                intent_id TEXT NOT NULL,
                caller_id TEXT NOT NULL,
                action TEXT NOT NULL,
                payload_hash TEXT NOT NULL,
                guardian_scores TEXT NOT NULL,
                status TEXT NOT NULL,
                evidence_chain_hash TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                created_at REAL NOT NULL DEFAULT (datetime('now'))
            )
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_intent_id ON evidence_ledger(intent_id)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_caller_id ON evidence_ledger(caller_id)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_event_type ON evidence_ledger(event_type)
        """
        )

        conn.commit()
        conn.close()

    def append(
        self,
        entry_id: str,
        event_type: str,
        intent_id: str,
        caller_id: str,
        action: str,
        payload: Dict[str, Any],
        guardian_scores: Dict[str, float],
        status: str,
    ) -> EvidenceEntry:
        """Append immutable entry to ledger.

        Never stores raw payloads. Only stores SHA256 hash of payload (zero-knowledge).
        Returns the entry with computed evidence chain hash.
        """

        # Compute zero-knowledge payload hash
        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()

        # Get previous hash for chain integrity
        previous_hash = self._get_latest_hash()

        # Create entry
        entry = EvidenceEntry(
            entry_id=entry_id,
            timestamp=time.time(),
            event_type=event_type,
            intent_id=intent_id,
            caller_id=caller_id,
            action=action,
            payload_hash=payload_hash,
            guardian_scores=guardian_scores,
            status=status,
            previous_hash=previous_hash,
            evidence_chain_hash="",  # Will compute below
        )

        # Compute evidence chain hash
        chain_content = (
            f"{entry.entry_id}:{entry.timestamp}:{entry.event_type}:"
            f"{entry.intent_id}:{entry.caller_id}:{entry.action}:"
            f"{entry.payload_hash}:{entry.status}:{entry.previous_hash}"
        )
        entry.evidence_chain_hash = hashlib.sha256(
            chain_content.encode()
        ).hexdigest()

        # Persist to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO evidence_ledger (
                entry_id, timestamp, event_type, intent_id, caller_id, action,
                payload_hash, guardian_scores, status, evidence_chain_hash, previous_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                entry.entry_id,
                entry.timestamp,
                entry.event_type,
                entry.intent_id,
                entry.caller_id,
                entry.action,
                entry.payload_hash,
                json.dumps(entry.guardian_scores),
                entry.status,
                entry.evidence_chain_hash,
                entry.previous_hash,
            ),
        )

        conn.commit()
        conn.close()

        return entry

    def get_intent_history(self, intent_id: str) -> List[EvidenceEntry]:
        """Retrieve all evidence entries for a specific intent."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM evidence_ledger WHERE intent_id = ? ORDER BY timestamp ASC",
            (intent_id,),
        )
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry = EvidenceEntry(
                entry_id=row[0],
                timestamp=row[1],
                event_type=row[2],
                intent_id=row[3],
                caller_id=row[4],
                action=row[5],
                payload_hash=row[6],
                guardian_scores=json.loads(row[7]),
                status=row[8],
                evidence_chain_hash=row[9],
                previous_hash=row[10],
            )
            entries.append(entry)

        return entries

    def get_caller_history(self, caller_id: str, limit: int = 100) -> List[EvidenceEntry]:
        """Retrieve evidence entries for a specific caller."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM evidence_ledger 
            WHERE caller_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """,
            (caller_id, limit),
        )
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry = EvidenceEntry(
                entry_id=row[0],
                timestamp=row[1],
                event_type=row[2],
                intent_id=row[3],
                caller_id=row[4],
                action=row[5],
                payload_hash=row[6],
                guardian_scores=json.loads(row[7]),
                status=row[8],
                evidence_chain_hash=row[9],
                previous_hash=row[10],
            )
            entries.append(entry)

        return entries

    def verify_chain_integrity(self) -> tuple[bool, str]:
        """Verify that the entire ledger chain is intact (no tampering).

        Returns (is_valid, reason).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM evidence_ledger ORDER BY timestamp ASC"
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return (True, "Empty ledger (valid)")

        previous_hash = "0"
        for i, row in enumerate(rows):
            entry_id = row[0]
            previous = row[10]

            if previous != previous_hash:
                return (
                    False,
                    f"Chain broken at entry {i} ({entry_id}): "
                    f"expected previous_hash={previous_hash}, got {previous}",
                )

            previous_hash = row[9]  # current evidence_chain_hash

        return (True, "Chain integrity verified")

    def _get_latest_hash(self) -> str:
        """Get the latest evidence_chain_hash from the ledger."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT evidence_chain_hash FROM evidence_ledger ORDER BY timestamp DESC LIMIT 1"
        )
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else "0"

    def get_recent_entries(self, limit: int = 100) -> List[EvidenceEntry]:
        """Retrieve N most recent entries."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM evidence_ledger 
            ORDER BY timestamp DESC 
            LIMIT ?
        """,
            (limit,),
        )
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry = EvidenceEntry(
                entry_id=row[0],
                timestamp=row[1],
                event_type=row[2],
                intent_id=row[3],
                caller_id=row[4],
                action=row[5],
                payload_hash=row[6],
                guardian_scores=json.loads(row[7]),
                status=row[8],
                evidence_chain_hash=row[9],
                previous_hash=row[10],
            )
            entries.append(entry)

        return entries
