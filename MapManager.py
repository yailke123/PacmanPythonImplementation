class MapManager:
	START_X = 9
	START_Y = 15

	def __init__(self, level_layout):
		# Removes blank edges from the initial layout.
		self.layout = [row[1:-1] for row in level_layout[2:]]

		# replaces initial pacman with blank value.
		self.layout[self.START_Y][self.START_X] = 9

	def move_pacman(self, new_x, new_y):
		if self.layout[new_y][new_x] == 0:
			self.layout[new_y][new_x] = 9
		print(self.layout[new_y])

	def calc_distance_to_closest_pellet(self, pacman_x, pacman_y):
		pass

	def get_closest_pellet_direction(self):
		pass

	def check_walls(self):
		pass
