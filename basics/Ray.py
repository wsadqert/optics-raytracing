import math
from math import pi

from .Basic2D import Basic2D
from .Point import Point

__all__ = ["Ray"]

class Ray(Basic2D):
	def __init__(self):
		self.x1: float = 0
		self.y1: float = 0
		self.x2: float = 0
		self.y2: float = 0
		self.angle: float = 0
		self.length: float = 0
		self.intensity: float = 1
	
	@classmethod
	def from_points(cls, point_1: Point, point_2: Point, intensity: float = 1):
		self = cls.__new__(cls)

		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_2.x
		self.y2 = point_2.y

		self.angle = math.degrees(math.atan2(self.y2 - self.y1, self.x2 - self.x1))
		self.length = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
		self.intensity = intensity

		return self

	@classmethod
	def from_polar(cls, point_1: Point, length: float, angle: float, intensity: float = 1):
		self = cls.__new__(cls)
		
		angle_rad = math.radians(angle)

		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_1.x + length * math.cos(angle_rad)
		self.y2 = point_1.y + length * math.sin(angle_rad)
		self.angle = angle
		self.length = length
		self.intensity = intensity

		return self
	
	@classmethod
	def from_angle(cls, point_1: Point, angle: float, intensity: float = 1):
		self = cls.__new__(cls)
		
		length = 1000
		angle_rad = math.radians(angle)

		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_1.x + length * math.cos(angle_rad)
		self.y2 = point_1.y + length * math.sin(angle_rad)
		self.angle = angle
		self.length = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
		self.intensity = intensity

		return self

	def modify(self, parameter: str, new_value):
		match parameter:
			case "angle":
				# saving point_1, length
				self.angle = new_value
				self.x2 = self.x1 + self.length * math.cos(math.radians(self.angle))
				self.y2 = self.y1 + self.length * math.sin(math.radians(self.angle))

			case "length":
				# saving point_1, angle
				self.length = new_value
				self.x2 = self.x1 + self.length * math.cos(math.radians(self.angle))
				self.y2 = self.y1 + self.length * math.sin(math.radians(self.angle))

			case "point_1":
				# saving point_2
				self.x1 = new_value.x
				self.y1 = new_value.y
				self.angle = math.degrees(math.atan2(self.y2 - self.y1, self.x2 - self.x1))
				self.length = math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

			case "point_2":
				# saving point_1
				self.x2 = new_value.x
				self.y2 = new_value.y
				self.angle = math.degrees(math.atan2(self.y2 - self.y1, self.x2 - self.x1))
				self.length = math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)
			
			case "intensity":
				self.intensity = new_value
			
			case _:
				raise ValueError("Invalid parameter")

	def get_points(self):
		return (
			Point(self.x1, self.y1),
			Point(self.x2, self.y2)
		)

	def __add__(self, other: Point):
		return self.move(other.x, other.y)

	def __str__(self) -> str:
		return f"Ray: \n\tPoint 1: {self.x1}, {self.y1}\n\tPoint 2: {self.x2}, {self.y2}\n\tAngle: {self.angle}\n\tLength: {self.length}"
