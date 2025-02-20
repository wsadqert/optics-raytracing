import math

from .Basic2D import Basic2D
from .Point import Point

__all__ = ["Segment"]

class Segment(Basic2D):
	def __init__(self, point_1: Point, point_2: Point):
		self.x1 = point_1.x
		self.y1 = point_1.y

		self.x2 = point_2.x
		self.y2 = point_2.y
	
	@classmethod
	def from_points(cls, point_1: Point, point_2: Point):
		return cls(point_1, point_2)
	
	@classmethod
	def from_polar(cls, point_1: Point, angle: float, length: float):
		angle_rad = math.radians(angle)

		x2 = point_1.x + length * math.cos(angle_rad)
		y2 = point_1.y + length * math.sin(angle_rad)
		return cls(point_1, Point(x2, y2))

	@property
	def angle(self):
		return math.degrees(math.atan2(self.y2 - self.y1, self.x2 - self.x1))

	@property
	def length(self):
		return math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)

	def get_points(self):
		return (
			Point(self.x1, self.y1), 
			Point(self.x2, self.y2)
		)

	# AI-GENERATED - Blackbox (https://www.blackbox.ai/chat/PJuvsbV)
	def __contains__(self, point: Point):
		# print(self.get_points())
		# print(point.x, point.y, self.x1, self.y1, self.x2, self.y2)

		if min(self.x1, self.x2) <= point.x <= max(self.x1, self.x2) and min(self.y1, self.y2) <= point.y <= max(self.y1, self.y2):
			# Calculate the cross product to check if the point is on the line
			cross_product = (self.y2 - self.y1) * (point.x - self.x1) - (self.x2 - self.x1) * (point.y - self.y1)
			
			print(cross_product)

			# Check if the cross product is close to zero (indicating collinearity)
			if abs(cross_product) < 1e-9:  # A small tolerance for floating-point comparison
				return True
		
		return False

	def __str__(self):
		return f"Segment from ({self.x1}, {self.y1}) to ({self.x2}, {self.y2})"

	def __repr__(self):
		return self.__str__()
