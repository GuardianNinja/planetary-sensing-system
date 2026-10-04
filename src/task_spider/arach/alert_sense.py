"""
Arach Alert Sense
Gentle, contextual notifications based on Spider Sense.

Blueprint anchor:
"Proactive but gentle notification system… always asks, never demands."
"""

from enum import Enum
import time


class Sensitivity(Enum):
    QUIET_WEB = "QUIET_WEB"
    GENTLE_HUM = "GENTLE_HUM"
    ACTIVE_HUNT = "ACTIVE_HUNT"


class InformationEmergency(Enum):
    NONE = "NONE"
    CONFLICT = "CONFLICT"
    CRITICAL = "CRITICAL"


class AlertSense:
    def __init__(self, sensitivity: Sensitivity = Sensitivity.GENTLE_HUM):
        self.sensitivity = sensitivity
        self.last_alert_time = 0

    def should_alert(self) -> bool:
        """Rate‑limit alerts to avoid intrusiveness."""
        return (time.time() - self.last_alert_time) > 5

    def notify(self, message: str, emergency: InformationEmergency = InformationEmergency.NONE):
        if not self.should_alert():
            return None

        self.last_alert_time = time.time()

        return {
            "timestamp": self.last_alert_time,
            "message": message,
            "emergency": emergency.value,
            "sensitivity": self.sensitivity.value,
        }

    def set_sensitivity(self, level: Sensitivity):
        self.sensitivity = level
