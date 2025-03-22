from .abc import Active
from basics import *
from geometry import ray_segment_intersection

__all__ = ["Splitter"]

class Splitter(Active):
	def __init__(self, name: str, center: Point, size: float, angle: float, reflect_ratio: float = 0.5, *args, **kwargs):
		super().__init__(name, center, 0, size, angle, *args, **kwargs)

		self.reflect_ratio = max(reflect_ratio, 0)
		self.reflect_ratio = min(self.reflect_ratio, 1)
	
	def apply(self, ray: Ray):
		lens_segment = self.to_segment()

		intersect_point = ray_segment_intersection(lens_segment, ray)

		if intersect_point is None:
			return ray
		
		new_angle = 2 * self.angle - ray.angle % 360
		reflected_ray = Ray.from_angle(intersect_point, new_angle, ray.intensity * self.reflect_ratio)
		continued_ray = Ray.from_angle(intersect_point, ray.angle, ray.intensity)

		return [reflected_ray, continued_ray]
