import math

from .abc import Active
from basics import *
from geometry import ray_segment_intersection, calculate_point_segment_distance

__all__ = ["Mirror"]

class Mirror(Active):
	def __init__(self, name: str, center: Point, size: float, angle: float, *args, **kwargs):
		super().__init__(name, center, size, size, angle, *args, **kwargs)

		self.size = size

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
	
	def apply(self, ray: Ray):
		lens_segment = self.to_segment()

		intersect_point = ray_segment_intersection(lens_segment, ray)

		if intersect_point is None:
			return ray
		
		new_angle = 2 * self.angle - ray.angle
		new_ray = Ray.from_angle(intersect_point, new_angle)

		return new_ray
