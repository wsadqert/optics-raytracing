import numpy as np

from geometry.geometry import iterate_over_length

from .abc import Source
from basics import Ray, Point

__all__ = ["Beam"]

class Beam(Source):
	def __init__(self, name, point: Point, angle: float, size: float, intensity = 1.):
		super().__init__(name, point, intensity=intensity, angle=angle, size=size)

		self.NUM_RAYS = 20

	def get_rays(self):
		return [
			Ray.from_angle(point, self.angle + 90)
			for point in iterate_over_length(self.to_segment(), step=self.size / self.NUM_RAYS)
		]
