from math import radians
from random import randint

from ..fov import compute_fov, compute_fov_angled


def generate_facing():
    return radians(randint(0, 7) * 45)


class Sight:
    def __init__(
        self,
        fov_radius=10,
        fov_span=radians(135),
        facing=generate_facing(),
        degrees=False,
    ):
        self.fov_radius = fov_radius
        if degrees:
            self.fov_span = radians(fov_span)
        else:
            self.fov_span = fov_span
        self.facing = facing

    def face(self, facing):
        if self.facing is facing:
            return False

        self.facing = facing
        return True

    def get_fov(self, fov_map, memory=None):
        compute_fov(
            fov_map, self.owner.x, self.owner.y, self.fov_radius, memory=memory
        )

    def get_fov_angled(self, fov_map, memory=None):
        compute_fov_angled(
            fov_map,
            self.owner.x,
            self.owner.y,
            self.fov_radius,
            self.facing,
            self.fov_span,
            memory=memory,
        )
