// @ts-expect-error: GuardianIsopod may not be exported yet
import { GuardianIsopod } from "./guardianIsopod";

// Define or import IsopodSensors and IsopodOutputs if not already available
type IsopodSensors = {
  timeOfDay: string;
  proximityToKid: number;
  // ...other sensor fields as needed
};

type IsopodOutputs = {
  leds: string;
  sound: string;
  posture: string;
  bounceFactor: number;
  // ...other output fields as needed
};

// Remove the import since IsopodSensors is not exported from guardianIsopod
// import type { IsopodSensors } from "./guardianIsopod";

// Import or define IsopodSensors and IsopodOutputs if not already imported

class GuardianIsopodWithMemory extends GuardianIsopod {
  private checkIns = 0;

  public nightlyCheckIn(sensors: IsopodSensors): IsopodOutputs {
    this.checkIns++;

    // At night, if far from kid, encourage reconnection
    if (sensors.timeOfDay === "NIGHT" && sensors.proximityToKid < 0.3) {
      return {
        leds: "PULSE",
        sound: "CHIRP",
        posture: "ROLLED",
        bounceFactor: 0.4,
      };
    }

    // If close, just glow softly
    return super.update({ ...sensors, timeOfDay: "NIGHT" });
  }
}
