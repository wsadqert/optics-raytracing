from abc import ABC, abstractmethod
from basics import Point, Segment

__all__ = ["Component"]

class Component(ABC):
	def __init__(self, name: str, point: Point, *args, **kwargs):
		self.name = name
		self.x = point.x
		self.y = point.y
		self.args = args

		for key, value in kwargs.items():
			setattr(self, key, value)
	
	@abstractmethod
	def to_points(self) -> list[Point]:
		pass
	
	def to_segment(self) -> Segment:
		points = self.get_points()

		if len(points) != 2:
			raise ValueError(f"cannot create Segment, 2 points expected, {len(points)} given")
		
		return Segment.from_points(*points)

	@property
	def point(self):
		return Point(self.x, self.y)
