export type IsopodState = "PLAY" | "CURIOUS" | "DEFENSIVE" | "GUARDIAN";

export interface IsopodSensors {
  touchIntensity: number;   // 0–1
  shakeLevel: number;       // 0–1
  proximityToKid: number;   // 0–1
  ambientNoise: number;     // 0–1
  timeOfDay: "DAY" | "NIGHT";
}

export interface IsopodOutputs {
  leds: "OFF" | "SOFT_GLOW" | "PULSE" | "ALERT";
  sound: "NONE" | "CHIRP" | "PURR" | "WARN";
  posture: "ROLLED" | "HALF_OPEN" | "OPEN";
  bounceFactor: number;
}

export class GuardianIsopod {
  private state: IsopodState = "PLAY";

  public update(sensors: IsopodSensors): IsopodOutputs {
    this.state = this.nextState(this.state, sensors);
    return this.render(this.state);
  }

  private nextState(current: IsopodState, s: IsopodSensors): IsopodState {
    if (s.shakeLevel > 0.8 || s.ambientNoise > 0.8) return "DEFENSIVE";

    if (s.timeOfDay === "NIGHT" && s.proximityToKid > 0.7) return "GUARDIAN";

    if (s.touchIntensity > 0.3 && s.touchIntensity <= 0.8) return "CURIOUS";

    return "PLAY";
  }

  private render(state: IsopodState): IsopodOutputs {
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
