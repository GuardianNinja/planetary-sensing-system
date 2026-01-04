
const GuardianIsopod = require("../guardianIsopod");

// If GuardianIsopod exports a function named 'update', use it directly
// Otherwise, adjust according to the actual export

const iso = GuardianIsopod;

const sampleSensors = {
  touchIntensity: 0.5,
  shakeLevel: 0.1,
  proximityToKid: 0.9,
  ambientNoise: 0.2,
  timeOfDay: "NIGHT" as const,
};

console.log("Isopod output:", iso.update(sampleSensors));
