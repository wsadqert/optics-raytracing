from .abc import Source
from basics import Ray, Point

__all__ = ["Laser"]

class Laser(Source):
	def __init__(self, name: str, point: Point, angle: float, intensity = 1.):
		super().__init__(name, point, intensity=intensity, angle=angle)

	def to_points(self):
		return [self.point]

	def get_rays(self) -> list[Ray]:
		return [Ray.from_angle(Point(self.x, self.y), self.angle), ]
