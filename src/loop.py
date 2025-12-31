# src/loop.py
from typing import Iterable, List
from .models import RawSignal, VerifiedRecord
from .verification import (
    JarvondisVerifier,
    KrystalVerifier,
    MikoVerifier,
    build_triple_verdict,
)
from .firewall import GyroscopicFirewall


class TripleVerificationLoop:
    """
    Runs the forward and backward triple-verification process.
    """

    def __init__(self):
        self.jarvondis = JarvondisVerifier()
        self.krystal = KrystalVerifier()
        self.miko = MikoVerifier()
        self.firewall = GyroscopicFirewall()

    def forward_pass(self, signals: Iterable[RawSignal]) -> List[VerifiedRecord]:
        results: List[VerifiedRecord] = []
        for step, signal in enumerate(signals):
            fw_state = self.firewall.next_state(step)
            structural = self.jarvondis.verify(signal)
            clarity = self.krystal.verify(signal)
            experience = self.miko.verify(signal)

            firewall_state_str = f"{fw_state.axis}:{fw_state.seed}"
            triple = build_triple_verdict(
                structural=structural,
                clarity=clarity,
                experience=experience,
                firewall_state=firewall_state_str,
            )

            record = VerifiedRecord(
                timestamp=signal.timestamp,
                node_id=signal.node_id,
                element=signal.element,
                input_payload=signal.payload,
                verdicts=triple,
            )
            results.append(record)
        return results

    def backward_pass(self, records: Iterable[VerifiedRecord]) -> List[VerifiedRecord]:
        """
        Re-run verification on the existing records in reverse order.
        This lets you compare forward vs backward results.
        """
        rechecked: List[VerifiedRecord] = []
        for step, record in enumerate(reversed(list(records))):
            fw_state = self.firewall.next_state(step)
            signal = RawSignal(
                timestamp=record.timestamp,
                node_id=record.node_id,
                element=record.element,
                payload=record.input_payload,
            )
            structural = self.jarvondis.verify(signal)
            clarity = self.krystal.verify(signal)
            experience = self.miko.verify(signal)

            firewall_state_str = f"{fw_state.axis}:{fw_state.seed}"
            triple = build_triple_verdict(
                structural=structural,
                clarity=clarity,
                experience=experience,
                firewall_state=firewall_state_str,
            )

            updated_record = VerifiedRecord(
                timestamp=record.timestamp,
                node_id=record.node_id,
                element=record.element,
                input_payload=record.input_payload,
                verdicts=triple,
            )
            rechecked.append(updated_record)
        return rechecked
