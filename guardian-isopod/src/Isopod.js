"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class GuardianIsopod {
    state = "PLAY";
    constructor() { }
    update(sensors) {
        this.state = this.nextState(this.state, sensors);
        return this.render(this.state, sensors);
    }
    nextState(current, s) {
        // If shaken hard or loud environment → defensive ball
        if (s.shakeLevel > 0.8 || s.ambientNoise > 0.8) {
            return "DEFENSIVE";
        }
        // At night, close to kid → guardian mode
        if (s.timeOfDay === "NIGHT" && s.proximityToKid > 0.7) {
            return "GUARDIAN";
        }
        // Gentle touch → curious buddy
        if (s.touchIntensity > 0.3 && s.touchIntensity <= 0.8) {
            return "CURIOUS";
        }
        // Default → playful ball
        return "PLAY";
    }
    render(state, s) {
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
                    bounceFactor: 0.2, // more “heavy”, less bouncy
                };
            case "GUARDIAN":
                return {
                    leds: "SOFT_GLOW",
                    sound: "PURR",
                    posture: "OPEN",
                    bounceFactor: 0.1, // mostly stays put
                };
        }
    }
}
//# sourceMappingURL=Isopod.js.map