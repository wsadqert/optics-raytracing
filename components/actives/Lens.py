import math

from geometry import calculate_point_segment_distance
from .abc import Active
from basics import *

__all__ = ["Lens"]

class Lens(Active):
	def __init__(self, name: str, center: Point, radius: float, angle: float, focus: float, *args, **kwargs):
		super().__init__(name, center, 0, 2*radius, angle, *args, **kwargs)

		self.focus = focus

	def apply(self, ray: Ray) -> Ray:
		lens_segment = self.to_segment()

		# TODO: implement lens behaviour
		
		ray.move(100, 100)
		return ray
