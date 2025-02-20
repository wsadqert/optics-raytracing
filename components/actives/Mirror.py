
from .abc import Active
from basics import *
from geometry import ray_segment_intersection

__all__ = ["Mirror"]

class Mirror(Active):
	def __init__(self, name: str, center: Point, size: float, angle: float, *args, **kwargs):
		super().__init__(name, center, 0, size, angle, *args, **kwargs)
	
	def apply(self, ray: Ray):
		lens_segment = self.to_segment()

		intersect_point = ray_segment_intersection(lens_segment, ray)

		if intersect_point is None:
			return ray
		
		new_angle = 2 * self.angle - ray.angle % 360
		new_ray = Ray.from_angle(intersect_point, new_angle)

		return new_ray
