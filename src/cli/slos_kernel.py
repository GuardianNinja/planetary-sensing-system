import json
import sys
from slos_kernel.orchestrator import IntentPacket, build_kernel_for_world

def main():
    world_id = sys.argv[1] if len(sys.argv) > 1 else "WORLD-LOCAL"
    kernel = build_kernel_for_world(world_id=world_id, display_name="Captain")

    raw = sys.stdin.read()
    data = json.loads(raw)

    packet = IntentPacket(
        intent_id=data.get("intent_id", "auto"),
        caller_id=data.get("caller_id", "local-cli"),
        action=data["action"],
        payload=data.get("payload", {}),
        signature="DEV-MODE",
    )

    receipt = kernel.process_intent(packet)
    print(json.dumps({
        "intent_id": receipt.intent_id,
        "status": receipt.execution_status,
        "evidence_hash": receipt.evidence_hash,
        "result": receipt.result_payload,
    }))

if __name__ == "__main__":
    main()
