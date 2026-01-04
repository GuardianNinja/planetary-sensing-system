"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// @ts-expect-error: GuardianIsopod may not be exported yet
const guardianIsopod_1 = require("./guardianIsopod");
// Remove the import since IsopodSensors is not exported from guardianIsopod
// import type { IsopodSensors } from "./guardianIsopod";
// Import or define IsopodSensors and IsopodOutputs if not already imported
class GuardianIsopodWithMemory extends guardianIsopod_1.GuardianIsopod {
    checkIns = 0;
    nightlyCheckIn(sensors) {
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
//# sourceMappingURL=Guardian%20companion%20flavor.js.map