"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function applyBounce(physics, surfaceRestitution, isRolled) {
    const bounceMultiplier = isRolled ? 1.0 : 0.3; // open isopod absorbs more impact
    const newVelocityY = -physics.velocity.y * surfaceRestitution * bounceMultiplier;
    return {
        position: physics.position,
        velocity: {
            x: physics.velocity.x,
            y: newVelocityY,
        },
    };
}
//# sourceMappingURL=ball%20form.js.map