from abc import abstractmethod

from components import Component
from basics import Point, Ray

class Source(Component):
	def __init__(self, name: str, point: Point, angle: float, size_x: float, size_y: float, *args, intensity: float = 1., **kwargs):
		super().__init__(name, point, angle, size_x, size_y, *args, **kwargs)

		self.intensity: float = intensity
	
	def get_points(self) -> list[Point]:
		return [self.point]

	@abstractmethod
	def get_rays(self) -> list[Ray]:
		return []
