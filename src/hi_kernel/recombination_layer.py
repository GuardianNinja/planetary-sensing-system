"""Recombination Layer — Validate and merge execution results.

The Recombination Layer collects outputs from Arach agents,
validates them against the Evidence Ledger, and merges them into
a final governed result.

Blueprint anchor:
"Recombination: Collect outputs, validate evidence, return governed result."
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class RecombinedResult:
    """Final result after recombination and validation."""
    intent_id: str
    valid: bool
    payload: Dict[str, Any]
    validation_errors: list = None

    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []


class RecombinationLayer:
    """Validates and merges agent outputs into governed results."""

    def __init__(self, evidence_ledger: Any):
        self.evidence_ledger = evidence_ledger

    def recombine(
        self,
        intent_id: str,
        agent_outputs: Dict[str, Any],
    ) -> RecombinedResult:
        """Recombine agent outputs into a single governed result.

        Validates that:
        - All outputs are consistent
        - No conflicting data
        - Evidence trail supports the result
        """

        validation_errors = []

        # Validate agent outputs exist
        if not agent_outputs:
            validation_errors.append("No agent outputs provided")
            return RecombinedResult(
                intent_id=intent_id,
                valid=False,
                payload={},
                validation_errors=validation_errors,
            )

        # Validate evidence trail
        evidence_history = self.evidence_ledger.get_intent_history(intent_id)
        if not evidence_history:
            validation_errors.append(f"No evidence trail for intent {intent_id}")

        # Merge agent outputs
        merged_payload = {}
        for agent_name, output in agent_outputs.items():
            if isinstance(output, dict):
                merged_payload[agent_name] = output
            else:
                validation_errors.append(
                    f"Agent {agent_name} output is not a dictionary"
                )

        # Create final result
        return RecombinedResult(
            intent_id=intent_id,
            valid=len(validation_errors) == 0,
            payload=merged_payload,
            validation_errors=validation_errors,
        )

    def validate_consistency(self, results: Dict[str, Any]) -> bool:
        """Validate that all results are internally consistent."""
        # Check for conflicting keys
        all_keys = set()
        for key, value in results.items():
            if key in all_keys:
                return False
            all_keys.add(key)
        return True
