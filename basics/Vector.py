import math
from dataclasses import dataclass
from typing import Union

from .Basic2D import Basic2D
from .Segment import Segment
from .Point import Point

__all__ = ["Vector"]


@dataclass
class Vector(Basic2D):
	x: float = 0
	y: float = 0

	def rotate(self, angle: float) -> "Vector":
		"""
		Rotates the vector counterclockwise by the given angle in degrees.
		"""

		angle = math.radians(angle)

		return Vector(
			self.x * math.cos(angle) - self.y * math.sin(angle),
			self.x * math.sin(angle) + self.y * math.cos(angle),
		)
	
	@classmethod
	def from_points(cls, point_1: Point, point_2: Point):
		return cls(point_2.x - point_1.x, point_2.y - point_1.y)

	@classmethod
	def from_segment(cls, segment: Segment):
		return cls.from_points(*segment.get_points())
	
	@classmethod
	def from_point(cls, point: Point):
		return cls(point.x, point.y)
	
	@classmethod
	def from_polar(cls, length: float, angle: float):
		return cls(
			length * math.cos(math.radians(angle)), 
			length * math.sin(math.radians(angle))
		)
	
	def get_points(self):
		return [Point(self.x, self.y),]
	
	def __neg__(self) -> "Vector":
		return Vector(-self.x, -self.y)

	def __add__(self, other: Union["Vector", Point]) -> "Vector":
		return Vector(self.x + other.x, self.y + other.y)

	def __radd__(self, other: Point) -> "Vector":
		return self + other

	def __sub__(self, other: Union["Vector", Point]) -> "Vector":
		return Vector(self.x - other.x, self.y - other.y)

	def __rsub__(self, other: Point) -> "Vector":
		return -(self - other)
	
	def __rsub__(self, other: Point) -> "Vector":
		return -(self - other)

	def __mul__(self, scalar: float) -> "Vector":
		return Vector(self.x * scalar, self.y * scalar)
	
	def __rmul__(self, scalar: float) -> "Vector":
		return self * scalar
	
	def __truediv__(self, scalar: float) -> "Vector":
		return Vector(self.x / scalar, self.y / scalar)

	def __eq__(self, other: "Vector") -> bool:
		if isinstance(other, int):
			if other == 0:
				return self == Vector(0, 0)
			else:
				return False

		elif isinstance(other, Vector):
			return self.x == other.x and self.y == other.y

		return False

	def __bool__(self):
		return self != Vector(0, 0)
