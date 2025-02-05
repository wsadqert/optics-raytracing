from abc import abstractmethod

from components.abc import Component
from basics import Ray, Point, Segment
from geometry import calculate_point_segment_distance

class Active(Component):
	def __init__(self, name: str, point: Point, size_x: float, size_y: float, angle: float, *args, **kwargs):
		super().__init__(name, point, *args, **kwargs)
		
		self.size_x = size_x
		self.size_y = size_y
		self.angle = angle

	@abstractmethod
	def apply(self, ray: Ray) -> Ray:
		pass

	def distance(self, point: Point) -> float:
		return calculate_point_segment_distance(point, self.to_segment())

	def to_segment(self) -> Segment:
		points = self.get_points()

		if len(points) != 2:
			raise ValueError(f"cannot create Segment, 2 points expected, {len(points)} given")
		
		return Segment.from_points(*points)
	