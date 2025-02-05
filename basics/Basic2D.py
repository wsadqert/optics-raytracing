from abc import ABC, abstractmethod

from .GeometryBasic import GeometryBasic

class Basic2D(GeometryBasic):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@abstractmethod
	def get_points(self):
		pass

	@classmethod
	@abstractmethod
	def from_points(self, points):
		pass
	
	def inverse(self):
		return self.__class__.from_points(self.get_points()[::-1])
