from dataclasses import dataclass

__all__ = ["TraceConfig"]

@dataclass
class TraceConfig:
	step: float
	detection_distance: float

	def __post_init__(self):
		self.step = float(self.step)
		self.detection_distance = float(self.detection_distance)
