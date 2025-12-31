# src/firewall.py
import random
from dataclasses import dataclass
from typing import Dict, Any


GYRO_AXES = ["identity_focus", "route_focus", "anomaly_focus"]


@dataclass
class FirewallState:
    axis: str
    seed: int


class GyroscopicFirewall:
    """
    Conceptual gyroscopic firewall.
    Rotates emphasis across axes over time.
    This is a placeholder, not real security code.
    """

    def __init__(self, base_seed: int = 42):
        self.base_seed = base_seed
        self._rng = random.Random(base_seed)

    def next_state(self, step: int) -> FirewallState:
        # Simple pseudo-random rotation dependent on step
        axis = GYRO_AXES[step % len(GYRO_AXES)]
        seed = self._rng.randint(0, 1_000_000)
        return FirewallState(axis=axis, seed=seed)

    def filter_signal(self, signal: Dict[str, Any], state: FirewallState) -> Dict[str, Any]:
        """
        Placeholder function to 'filter' or annotate signals.
        In a real system, this would enforce policies.
        """
        enriched = dict(signal)
        enriched["_firewall_axis"] = state.axis
        enriched["_firewall_seed"] = state.seed
        return enriched
