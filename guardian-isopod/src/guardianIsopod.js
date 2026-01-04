"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class GuardianIsopod {
    state = "PLAY";
    update(sensors) {
        this.state = this.nextState(this.state, sensors);
        return this.render(this.state);
    }
    nextState(current, s) {
        if (s.shakeLevel > 0.8 || s.ambientNoise > 0.8)
            return "DEFENSIVE";
        if (s.timeOfDay === "NIGHT" && s.proximityToKid > 0.7)
            return "GUARDIAN";
        if (s.touchIntensity > 0.3 && s.touchIntensity <= 0.8)
            return "CURIOUS";
        return "PLAY";
    }
    render(state) {
        switch (state) {
            case "PLAY":
                return {
                    leds: "OFF",
                    sound: "CHIRP",
                    posture: "ROLLED",
                    bounceFactor: 1.0,
                };
            case "CURIOUS":
                return {
                    leds: "PULSE",
                    sound: "PURR",
                    posture: "HALF_OPEN",
                    bounceFactor: 0.6,
                };
            case "DEFENSIVE":
                return {
                    leds: "ALERT",
                    sound: "WARN",
                    posture: "ROLLED",
                    bounceFactor: 0.2,
                };
            case "GUARDIAN":
                return {
                    leds: "SOFT_GLOW",
                    sound: "PURR",
                    posture: "OPEN",
                    bounceFactor: 0.1,
                };
        }
    }
}
//# sourceMappingURL=guardianIsopod.js.map