"""HI Kernel — Brainstem orchestrator of the digital civilization.

The HI Kernel is the unified operational core:
- Intent Interpreter: converts human intent to structured tasks
- Guardian Interceptor: triple-guardian evaluation
- Orchestrator: coordinates dispatch through Arach
- Recombination: validates and merges results

Blueprint anchor:
"HI Kernel → Task Spider → User World → Planetary Skin"
"""

from .intent_interpreter import IntentInterpreter, IntentPacket
from .guardian_interceptor import GuardianInterceptor
from .orchestrator import HIKernelOrchestrator
from .recombination_layer import RecombinationLayer

__all__ = [
    "IntentInterpreter",
    "IntentPacket",
    "GuardianInterceptor",
    "HIKernelOrchestrator",
    "RecombinationLayer",
]
