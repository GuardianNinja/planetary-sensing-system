interface Vector2 {
  x: number;
  y: number;
}

interface PhysicsState {
  position: Vector2;
  velocity: Vector2;
}

function applyBounce(
  physics: PhysicsState,
  surfaceRestitution: number,
  isRolled: boolean
): PhysicsState {
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
