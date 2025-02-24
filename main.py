import multiprocessing
from typing import Literal
from rich.traceback import install

install(show_locals=True, width=300)

from colorama import Fore as FORE
from tkinter import Tk

from queue import Queue
import threading

from parser import parse_config
from frontend import Drawer, InteractiveCanvas
from frontend import DrawerConfig, TraceConfig
from basics import *
from components import *
from geometry import *


class RayTracingApp:
	def __init__(self, master):
		self.master = master

		frontend_config_raw = parse_config(".config/frontend.cfg")
		trace_config_raw = parse_config(".config/raytrace.cfg")
		
		drawer_config = DrawerConfig(**frontend_config_raw['Drawer'])
		self.trace_config = TraceConfig(**trace_config_raw['raytrace'])

		self.canvas = InteractiveCanvas(master, dict(frontend_config_raw['tcl']))
		self.canvas.pack()

		self.drawer = Drawer(self.canvas, drawer_config)

		self.create_components()

		self.limits = {
			"min": self.components[0].get_points()[0], 
			"max": self.components[0].get_points()[0], 
		}

		max_size = -1
		
		# find bounding box
		for component in self.components:
			if max_size < component.size: max_size = component.size
			
			for point in component.get_points():
				min_x = min(self.limits["min"].x, point.x)
				min_y = min(self.limits["min"].y, point.y)
				max_x = max(self.limits["max"].x, point.x)
				max_y = max(self.limits["max"].y, point.y)
				
				self.limits[0] = Point(min_x, min_y)
				self.limits[1] = Point(max_x, max_y)

		# draw all components
		for component in self.components:
			self.drawer.draw_component(component)
		
		self.trace()
		self.draw_sources()

	def create_components(self):
		self.sources: list[Source] = [
			# Laser("Laser1", Point(400, 300), angle=0),
			# Lamp("Lamp1", Point(300, 300)),
			Beam("Beam1", Point(400, 300), angle=-90, size=100, amount_rays=10),
		]
		self.actives: list[Active] = [
			# Lens(name="Lens1", center=Point(500, 400), radius=100, angle=0, focus=500),
			Mirror(name="Mirror1", center=Point(500, 300), size=100, angle=45),
			Mirror(name="Mirror2", center=Point(500, 400), size=100, angle=45),
			# Mirror(name="Mirror1", center=Point(650, 400), size=100, angle=-90),
			# Wall(name="Wall1", center=Point(700, 400), size=100, angle=0),
		]

		self.components: list[Component] = self.sources + self.actives
		# self.drawer.draw_mirror(Mirror(name="Mirror1", center=Point(650, 400), size=100, angle=-90))

	def trace(self):
		tracing_queue = Queue()
		draw_list = []

		# add all rays from sources to queue
		for source in self.sources:
			for ray in source.get_rays():
				tracing_queue.put(ray)

		# real tracing!
		while not tracing_queue.empty():
			ray: Ray = tracing_queue.get()
			# print(ray)

			is_skipping = False

			for point_idx, current_point in iterate_over_length(Segment.from_points(*ray.get_points()), step=self.trace_config.step):
				# is current_point the intersection point?
				is_intersection_found = False

				close_to_actives: list[bool] = []  # for each active is the current_point close to the active

				for active in self.actives:
					is_close_to = (active.distance(current_point) < self.trace_config.detection_distance)
					close_to_actives.append(is_close_to)

					if point_idx == 0:
						is_skipping = is_close_to

					# if not skipping
					if is_close_to:
						if is_skipping:
							break

						new_ray = active.apply(ray)

						ray.modify("point_2", current_point)  # cropping existing ray at current_point
						draw_list.append(ray)
						tracing_queue.put(new_ray)

						is_intersection_found = True
						break
				
				if point_idx != 0 and not any(close_to_actives):
					is_skipping = False

				if is_intersection_found:
					# goto next ray
					break

			else:
				draw_list.append(ray)
		
		for ray in draw_list:
			self.drawer.draw_ray(ray)

	def draw_sources(self):
		for source in self.sources:
			self.drawer.draw_source(source)

	@classmethod
	def _run_app(cls):
		root = Tk()
		app = cls(root)
		root.mainloop()
	
	@classmethod
	def start(cls, parallel_mode: str = "none") -> threading.Thread | multiprocessing.Process | None:
		"""
		parallel_mode: str - one of:
			`thread` - to run in separate thread
			`process` - to run in separate process
			`none` - run in main thread (default)
		"""
		match parallel_mode:
			case "thread":
				thread = threading.Thread(target=cls._run_app)
				thread.start()
				return thread

			case "process":
				process = multiprocessing.Process(target=cls._run_app)
				process.start()
				return process

			case "none":
				cls._run_app()
			
			case _:
				raise ValueError

if __name__ == "__main__":
	app = RayTracingApp.start("process")
