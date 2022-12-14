from pygame import Color, Surface

from src import sounds
from src.hitboxes import Hitbox
from src.projectiles.base import Projectile


class HawkoLaser(Projectile):
    width = 150
    height = 10
    speed = 20

    def __init__(self, x, y, facing_right, owner):
        u = self.speed if facing_right else -self.speed
        super().__init__(x=x, y=y, u=u, v=0, owner=owner)
        self.image = Surface((150, 10))
        self.image.fill(Color("red"))
        self.active_hitboxes = [
            Hitbox(
                owner=self,
                x_offset=x_offset,
                width=30,
                height=30,
                base_knockback=20,
                knockback_angle=30,
                damage=3,
                sound=sounds.tap4,
            )
            for x_offset in [-75, 0, 75]
        ]
        if not facing_right:
            for hitbox in self.active_hitboxes:
                hitbox.flip_x()

    def handle_get_hit(self, hitbox):
        pass  # falco lasers can't be hit

    def handle_land_hit(self, hitbox):
        self.kill()  # falco lasers disappear on hit
