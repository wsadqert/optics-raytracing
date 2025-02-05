from rich.traceback import install

install(show_locals=True, width=300)

from tkinter import Tk
import numpy as np
from queue import Queue

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

		for component in self.components:
			self.drawer.draw_component(component)
		
		self.trace()
		self.draw_rays()

	def create_components(self):
		self.sources: list[Source] = [
			Laser("Laser1", Point(400, 300), angle=30),
			# Lamp("Lamp1", Point(300, 300)),
		]
		self.actives: list[Active] = [
			# Lens(name="Lens1", center=Point(500, 400), radius=100, angle=0, focus=500),
			Mirror(name="Mirror1", center=Point(600, 400), size=100, angle=0),
			# Wall(name="Wall1", center=Point(700, 400), size=100, angle=0),
		]

		self.components: list[Component] = self.sources + self.actives

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

			for current_point in iterate_over_length(Segment.from_points(*ray.get_points()), step=self.trace_config.step):
				is_intersection_found = False

				for active in self.actives:
					if active.distance(current_point) < self.trace_config.detection_distance:
						draw_list.append(active.apply(ray))

						ray.modify("point_2", current_point)
						draw_list.append(ray)

						is_intersection_found = True
						break
				
				if is_intersection_found:
					break
		
		for ray in draw_list:
			self.drawer.draw_ray(ray)

	def draw_rays(self):
		for source in self.sources:
			self.drawer.draw_source(source)


if __name__ == "__main__":
	root = Tk()
	app = RayTracingApp(root)
	root.mainloop()
