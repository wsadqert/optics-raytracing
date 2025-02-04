from rich.traceback import install
install(show_locals=True, width=300)

from tkinter import Tk
import numpy as np
from queue import Queue  # Import Queue

from parser import parse_config
from frontend import Drawer, InteractiveCanvas
from frontend import DrawerConfig, TraceConfig
from basics import *
from components import *


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
		self.draw_rays()

	def create_components(self):
		self.lasers = [
			Laser("Laser1", Point(400, 300), angle=30)
		]
		self.lamps = [
			# Lamp("Lamp1", Point(300, 300))
		]
		self.lenses = [
			# Lens(name="Lens1", center=Point(500, 400), radius=100, angle=0, focus=500)
		]
		self.mirrors = [
			Mirror(name="Mirror1", center=Point(600, 400), size=100, angle=0)
		]

		self.sources: list[Source] = self.lamps + self.lasers
		self.actives: list[Active] = self.lenses + self.mirrors

		# self.drawer.draw_lens(self.lenses[0])
		self.drawer.draw_mirror(self.mirrors[0])

		self.trace()

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

			for current_length in np.arange(0, ray.length, self.trace_config.step):
				current_point: Point = ray.get_points()[0] + Vector.from_polar(current_length, ray.angle)

				for active in self.actives:
					if active.distance(current_point) < self.trace_config.detection_distance:
						draw_list.append(active.apply(ray))

						ray.modify("point_2", current_point)
						draw_list.append(ray)

		for ray in draw_list:
			self.drawer.draw_ray(ray)

	def draw_rays(self):
		for source in self.sources:
			self.drawer.draw_source(source)


if __name__ == "__main__":
	root = Tk()
	app = RayTracingApp(root)
	root.mainloop()
