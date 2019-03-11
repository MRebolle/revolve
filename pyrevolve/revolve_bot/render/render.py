import cairo
from .canvas import Canvas
from .grid import Grid

class Render:

	def __init__(self):
		"""Instantiate grid"""
		self.grid = Grid()


	def parse_body_to_draw(self, canvas, module, slot):
		"""Parse the body to the canvas to draw the png"""
		if module.type == 'CoreComponent' or module.type == 'Core':
			canvas.draw_controller()
		elif module.type == 'ActiveHinge':
			canvas.move_by_slot(slot)
			Canvas.rotating_orientation += module.orientation
			canvas.draw_hinge(module.id)
			canvas.draw_connector_to_parent()
		elif module.type == 'FixedBrick':
			canvas.move_by_slot(slot)
			Canvas.rotating_orientation += module.orientation
			canvas.draw_module(module.id)
			canvas.draw_connector_to_parent()
		elif module.type == 'TouchSensor':
			canvas.move_by_slot(slot)			
			Canvas.rotating_orientation += module.orientation
			canvas.save_sensor_position()

		if module.has_children():
			# Traverse children of element to draw on canvas
			for core_slot, child_module in module.iter_children():
				if child_module is None:
					continue
				self.parse_body_to_draw(canvas, child_module, core_slot)		
			canvas.move_back()						
		else:
			# Element has no children, move back to previous state
			canvas.move_back()
				
	def traverse_path_of_robot(self, module, slot):
		"""Traverse path of robot to obtain visited coordinates"""		
		if module.type == 'ActiveHinge' or module.type == 'FixedBrick' or module.type == 'TouchSensor':
			self.grid.move_by_slot(slot)
			self.grid.add_to_visited()
		
		if module.has_children():
			# Traverse path of children of module
			for core_slot, child_module in module.iter_children():
				if child_module is None:
					continue
				self.traverse_path_of_robot(child_module, core_slot)	
			self.grid.move_back()						
		else:
			# Element has no children, move back to previous state
			self.grid.move_back()

	def render_robot(self, body, image_path):
		try:
			# Calculate dimensions of drawing and core position
			self.traverse_path_of_robot(body, 0)
			robot_dim = self.grid.calculate_grid_dimensions()
			width = abs(robot_dim[0] - robot_dim[1]) + 1
			height = abs(robot_dim[2] - robot_dim[3]) + 1
			core_position = [width - robot_dim[1] - 1, height - robot_dim[3] - 1]	

			# Draw canvas
			cv = Canvas(width, height, 100)
			cv.set_position(core_position[0], core_position[1])

			# Draw body of robot
			self.parse_body_to_draw(cv, body, 0)
			
			# Draw sensors after, so that they don't get overdrawn
			cv.draw_sensors()

			cv.save_png(image_path)

			# Reset variables to default values
			cv.reset_canvas()
			self.grid.reset_grid()
			

		except Exception as e: 
			print('Exception {}'.format(e))		