"use strict";
// physics.ts
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Apply a single physics step (simple gravity + ground bounce).
 * dt is "delta time" in seconds (e.g. 1/60 for ~60 FPS).
 */
function stepPhysics(state, config, dt, isRolled) {
    // 1. Apply gravity
    const vy = state.velocity.y + config.gravity * dt;
    // 2. Integrate position
    let newPos = {
        x: state.position.x + state.velocity.x * dt,
        y: state.position.y + vy * dt,
    };
    let newVel = { x: state.velocity.x, y: vy };
    // 3. Ground collision + bounce
    if (newPos.y <= config.groundY) {
        newPos.y = config.groundY;
        const bounceMultiplier = isRolled ? 1.0 : 0.3; // open isopod absorbs more
        newVel.y = -newVel.y * config.surfaceRestitution * bounceMultiplier;
        // Apply simple horizontal friction when touching the ground
        newVel.x = newVel.x * (1 - config.friction);
        if (Math.abs(newVel.x) < 0.001)
            newVel.x = 0;
    }
    return {
        position: newPos,
        velocity: newVel,
    };
}
/**
 * Helper to create a default physics config for the isopod toy.
 */
function createDefaultPhysicsConfig() {
    return {
        gravity: -9.8, // downward
        groundY: 0, // ground at y = 0
        surfaceRestitution: 0.7, // medium-bouncy
        friction: 0.1, // light friction
    };
}
module.exports = { stepPhysics, createDefaultPhysicsConfig };
//# sourceMappingURL=physics.js.map