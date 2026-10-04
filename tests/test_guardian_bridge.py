# tests/test_guardian_bridge.py
def test_guardian_bridge_integration():
    payload = {
        "intent_type": "demo.echo",
        "payload": {"message": "hello"},
        "metadata": {
            "sensors": {
                "touchIntensity": 0.5,
                "shakeLevel": 0.1,
                "proximityToKid": 0.9,
                "ambientNoise": 0.2,
                "timeOfDay": "NIGHT",
            }
        }
    }

    resp = client.post("/v1/intent", json=payload)
    assert resp.status_code == 200
    assert resp.json()["status"] == "SUCCESS"
