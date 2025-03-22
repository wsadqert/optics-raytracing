import math

from geometry import ray_segment_intersection
from .abc import Active
from basics import *

__all__ = ["Lens"]

class Lens(Active):
	def __init__(self, name: str, center: Point, radius: float, angle: float, focus: float, *args, **kwargs):
		super().__init__(name, center, 0, 2*radius, angle, *args, **kwargs)

		self.focus = focus

	def apply(self, ray: Ray) -> Ray:
		lens_segment = self.to_segment()

		intersection_point = ray_segment_intersection(lens_segment, ray)

		if intersection_point is None:
			return ray
		
		print(intersection_point)

		h = intersection_point.y - self.point.y  # Height of intersection

		ray_angle_rad = math.radians(ray.angle - (self.angle - 90))

		new_angle = math.atan(math.tan(ray_angle_rad) - h / self.focus)
		new_angle = math.degrees(new_angle) + (self.angle - 90)

		new_ray = Ray.from_angle(intersection_point, new_angle, ray.intensity)

		return [new_ray]
