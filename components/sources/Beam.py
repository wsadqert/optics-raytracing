import math

from geometry.geometry import iterate_over_length
from .abc import Source
from basics import Ray, Point, Segment

__all__ = ["Beam"]

class Beam(Source):
	def __init__(self, name, point: Point, angle: float, size: float, intensity = 1.):
		super().__init__(name, point, angle, 0, size, intensity=intensity)

		self.NUM_RAYS = 20

	def get_rays(self):
		return [
			Ray.from_angle(point, self.angle + 90)
			for _, point in iterate_over_length(self.to_segment(), step=self.size / self.NUM_RAYS)
		]
	
	def to_segment(self) -> Segment:
		return Segment.from_points(*self.get_points())

	def get_points(self) -> tuple[Point, Point]:
		angle_rad = math.radians(self.angle)
		
		x1 = self.x - self.size / 2 * math.cos(angle_rad)
		y1 = self.y - self.size / 2 * math.sin(angle_rad)
		x2 = self.x + self.size / 2 * math.cos(angle_rad)
		y2 = self.y + self.size / 2 * math.sin(angle_rad)

		return (
			Point(x1, y1),
			Point(x2, y2)
		)
