from abc import abstractmethod
import math

from components.abc import Component
from basics import Ray, Point
from geometry import calculate_point_segment_distance

class Active(Component):
	def __init__(self, name: str, point: Point, size_x: float, size_y: float, angle: float, *args, **kwargs):
		super().__init__(name, point, angle, size_x, size_y, *args, **kwargs)

	@abstractmethod
	def apply(self, ray: Ray) -> Ray:
		pass

	def distance(self, point: Point) -> float:
		return calculate_point_segment_distance(point, self.to_segment())

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
