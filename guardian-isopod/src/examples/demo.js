"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const guardianIsopod_1 = __importDefault(require("../guardianIsopod"));
const iso = new guardianIsopod_1.default();
const sampleSensors = {
    touchIntensity: 0.5,
    shakeLevel: 0.1,
    proximityToKid: 0.9,
    ambientNoise: 0.2,
    timeOfDay: "NIGHT",
};
console.log("Isopod output:", iso.update(sampleSensors));
//# sourceMappingURL=demo.js.map