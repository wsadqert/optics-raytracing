from dataclasses import dataclass
from typing import Union

from .GeometryBasic import GeometryBasic

__all__ = ["Point"]

@dataclass
class Point(GeometryBasic):
	x: float = 0
	y: float = 0

	def to_tuple(self) -> tuple[float, float]:
		return self.x, self.y

	def __add__(self, other: Union["Point", "Vector"]) -> "Point":
		return Point(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other: Union["Point", "Vector"]) -> "Point":
		return Point(self.x - other.x, self.y - other.y)

	def __eq__(self, other: "Point") -> bool:
		return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9

	def __mul__(self, scalar: float) -> "Point":
		return Point(self.x * scalar, self.y * scalar)
	
	def __truediv__(self, scalar: float) -> "Point":
		return Point(self.x / scalar, self.y / scalar)
