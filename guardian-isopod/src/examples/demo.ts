import { GuardianIsopod, IsopodSensors } from "../guardianIsopod";

const iso = new GuardianIsopod();

const sampleSensors: IsopodSensors = {
  touchIntensity: 0.5,
  shakeLevel: 0.1,
  proximityToKid: 0.9,
  ambientNoise: 0.2,
  timeOfDay: "NIGHT",
};

console.log("Isopod output:", iso.update(sampleSensors));
