// physics.ts

interface Vector2 {
  x: number;
  y: number;
}

interface PhysicsState {
  position: Vector2;
  velocity: Vector2;
}

/**
 * Basic physics config for the isopod ball.
 * You can tweak these numbers to change how "floaty" or "heavy" it feels.
 */
interface PhysicsConfig {
  gravity: number;            // positive value pulling down on y
  groundY: number;            // y-position of the "floor"
  surfaceRestitution: number; // how bouncy the surface is (0–1)
  friction: number;           // how quickly it slows on the ground (0–1)
}

/**
 * Apply a single physics step (simple gravity + ground bounce).
 * dt is "delta time" in seconds (e.g. 1/60 for ~60 FPS).
 */
function stepPhysics(
  state: PhysicsState,
  config: PhysicsConfig,
  dt: number,
  isRolled: boolean
): PhysicsState {
  // 1. Apply gravity
  const vy = state.velocity.y + config.gravity * dt;

  // 2. Integrate position
  let newPos: Vector2 = {
    x: state.position.x + state.velocity.x * dt,
    y: state.position.y + vy * dt,
  };

  let newVel: Vector2 = { x: state.velocity.x, y: vy };

  // 3. Ground collision + bounce
  if (newPos.y <= config.groundY) {
    newPos.y = config.groundY;

    const bounceMultiplier = isRolled ? 1.0 : 0.3; // open isopod absorbs more
    newVel.y = -newVel.y * config.surfaceRestitution * bounceMultiplier;

    // Apply simple horizontal friction when touching the ground
    newVel.x = newVel.x * (1 - config.friction);
    if (Math.abs(newVel.x) < 0.001) newVel.x = 0;
  }

  return {
    position: newPos,
    velocity: newVel,
  };
}

/**
 * Helper to create a default physics config for the isopod toy.
 */
function createDefaultPhysicsConfig(): PhysicsConfig {
  return {
    gravity: -9.8,          // downward
    groundY: 0,             // ground at y = 0
    surfaceRestitution: 0.7, // medium-bouncy
    friction: 0.1,          // light friction
  };
}

