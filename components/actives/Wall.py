from basics import *
from components.actives.abc import Active


class Wall(Active):
	def __init__(self, name: str, center: Point, size: float, angle: float, *args, **kwargs):
		super().__init__(name, center, 0, size, angle, *args, **kwargs)


	def apply(self, ray: Ray):
		return Ray()
