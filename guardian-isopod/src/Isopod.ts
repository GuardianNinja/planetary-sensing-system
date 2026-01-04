type IsopodState = "PLAY" | "CURIOUS" | "DEFENSIVE" | "GUARDIAN";

interface IsopodSensors {
  touchIntensity: number;   // 0–1
  shakeLevel: number;       // 0–1
  proximityToKid: number;   // 0–1 (1 = very close)
  ambientNoise: number;     // 0–1
  timeOfDay: "DAY" | "NIGHT";
}

interface IsopodOutputs {
  leds: "OFF" | "SOFT_GLOW" | "PULSE" | "ALERT";
  sound: "NONE" | "CHIRP" | "PURR" | "WARN";
  posture: "ROLLED" | "HALF_OPEN" | "OPEN";
  bounceFactor: number; // 0–1 how “bouncy” it behaves
}

class GuardianIsopod {
  private state: IsopodState = "PLAY";

  constructor() {}

  public update(sensors: IsopodSensors): IsopodOutputs {
    this.state = this.nextState(this.state, sensors);
    return this.render(this.state, sensors);
  }

  private nextState(current: IsopodState, s: IsopodSensors): IsopodState {
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

  private render(state: IsopodState, s: IsopodSensors): IsopodOutputs {
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
