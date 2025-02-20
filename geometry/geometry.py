from typing import Generator
import numpy as np
from basics import *

__all__ = ["calculate_ray_direction", "ray_segment_intersection", "calculate_point_segment_distance", "iterate_over_length"]

def calculate_ray_direction(ray: Ray) -> Vector:
	# Calculate the direction vector of the ray
	dx = ray.x2 - ray.x1
	dy = ray.y2 - ray.y1
	length = ray.length
	
	if length == 0:
		return Vector()  # The ray has no direction
	return Vector(dx / length, dy / length)

def ray_segment_intersection(segment: Segment, ray: Ray) -> Point | None:
	# Ray represented as P + tD, where P is the start point, D is the direction, and t is a scalar
	# Segment represented as A + u(B - A), where A is the start point, B is the end point, and u is a scalar

	ray_direction: Vector = calculate_ray_direction(ray)
	
	if not ray_direction:
		return None  # Invalid ray

	ray_start = ray.get_points()[0]

	# Ray start point
	P = ray_start.to_tuple()
	D = ray_direction.get_points()[0].to_tuple()

	# Segment start and end points
	A = segment.get_points()[0].to_tuple()
	B = segment.get_points()[1].to_tuple()

	# Calculate the denominator
	denom = D[0] * (B[1] - A[1]) - D[1] * (B[0] - A[0])
	if abs(denom) < 1e-10:  # Parallel lines
		return None

	# Calculate the parameters t and u
	t = ((A[0] - P[0]) * (B[1] - A[1]) - (A[1] - P[1]) * (B[0] - A[0])) / denom
	u = ((A[0] - P[0]) * D[1] - (A[1] - P[1]) * D[0]) / denom

	# Check if the intersection point is on the ray and the segment
	if t >= 0 and 0 <= u <= 1:
		intersection_x = P[0] + t * D[0]
		intersection_y = P[1] + t * D[1]
		return Point(intersection_x, intersection_y)

	return None

# AI-GENERATED - ChatGPT (https://chatgpt.com/share/67a24fc7-0408-8013-8b6d-da3bcfc3edcb)
def calculate_point_segment_distance(point: Point, segment: Segment) -> float:
	# Convert points to numpy arrays
	A = np.array(segment.get_points()[0].to_tuple())
	B = np.array(segment.get_points()[1].to_tuple())
	P = np.array(point.to_tuple())
	
	# Vector AB and AP
	AB = B - A
	AP = P - A
	
	# Squared length of segment AB
	AB_squared = np.dot(AB, AB)
	
	# Projection scalar (t) of P onto AB (normalized)
	t = np.dot(AP, AB) / AB_squared if AB_squared != 0 else -1
	
	# Clamp t to the segment range [0,1]
	t = max(0, min(1, t))
	
	# Find the closest point on the segment
	closest_point = A + t * AB
	
	# Return the Euclidean distance
	return np.linalg.norm(P - closest_point)

def iterate_over_length(segment: Segment, step: float = None, num_steps: int = None, direction: int = 1) -> Generator[tuple[int, Point], None, None]:
	if step is not None and num_steps is not None:
		raise ValueError("Cannot specify both `step` and `num_steps`")
	if step is None and num_steps is None:
		raise ValueError("Must specify either `step` or `num_steps`")
	if direction not in (1, -1):
		raise ValueError("Direction must be 1 or -1")
	
	point_1 = segment.get_points()[0]

	if num_steps is None:
		num_steps = int(segment.length // step)

	num_steps = max(1, num_steps)
	
	step: Vector = Vector.from_segment(segment) / num_steps

	for i in range(0, num_steps + 1):
		yield i, point_1 + i * step
