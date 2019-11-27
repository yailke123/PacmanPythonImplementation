class MapManager:
	START_X = 9
	START_Y = 15

	def __init__(self, level_layout):
		# Removes blank edges from the initial layout.
		self.layout = [row[1:-1] for row in level_layout[2:]]

		# replaces initial pacman with blank value.
		self.layout[self.START_Y][self.START_X] = 9

	def reset_map(self, level_layout):
		# Removes blank edges from the initial layout.
		self.layout = [row[1:-1] for row in level_layout[2:]]

		# replaces initial pacman with blank value.
		self.layout[self.START_Y][self.START_X] = 9

	def move_pacman(self, new_x, new_y, pacman):
		if self.layout[new_y][new_x] == 0:
			self.layout[new_y][new_x] = 9
			pacman.did_eat = True
		else:
			pacman.did_eat = False

		print(self.layout[new_y])

	def calc_distance_to_closest_pellet(self, pacman_x, pacman_y):
		pass


	def check_walls(self, pacman_x, pacman_y):
		result = [0, 0, 0, 0]
		if self.layout[pacman_y - 1][pacman_x] == 1:	# up
			result[2] = 1
		if self.layout[pacman_y + 1][pacman_x] == 1:  # down
			result[3] = 1
		if self.layout[pacman_y][pacman_x - 1] == 1:	# left
			result[0] = 1
		if self.layout[pacman_y][pacman_x + 1] == 1:  # up
			result[1] = 1
		return result

	def get_closest_pellet_direction(self, pacman_x, pacman_y):  # the name is misleadign at the moment
		pellets = [0, 0, 0, 0]
		pac_left_index = pacman_y - 1
		pac_right_index = pacman_y + 1
		pac_up_index = pacman_x - 1
		pac_down_index = pacman_x + 1

		if pac_right_index <= 18 and self.layout[pacman_x][pac_right_index] == 0:  # we have 19 columns in total
			pellets[0] = 1
		if pac_left_index >= 0 and self.layout[pacman_x][pac_left_index] == 0:
			pellets[1] = 1
		if pac_up_index >= 0 and self.layout[pac_up_index][pacman_y] == 0:
			pellets[2] = 1
		if pac_down_index <= 20 and self.layout[pac_down_index][pacman_y] == 0:  # we have 21 rows in total
			pellets[3] = 1

		return pellets
