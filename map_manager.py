from random import shuffle
from copy import deepcopy

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

		# print(self.layout[new_y])

	# pacman_row is the row in the layout.
	# pacman_col is the column in the layout.
	def calc_distance_to_closest_pellets(self, row, col):
		non_binary_inputs = False
		left_layout = deepcopy(self.layout)
		right_layout = deepcopy(self.layout)
		up_layout = deepcopy(self.layout)
		down_layout = deepcopy(self.layout)

		# Set pacman starting position as visited
		left_layout[row][col] = -1
		right_layout[row][col] = -1
		up_layout[row][col] = -1
		down_layout[row][col] = -1
		# Calculate distances
		left_distance = self.check_pellet_on_side(row, col-1, left_layout)
		right_distance = self.check_pellet_on_side(row, col+1, right_layout)
		up_distance = self.check_pellet_on_side(row-1, col, up_layout)
		down_distance = self.check_pellet_on_side(row+1, col, down_layout)

		if non_binary_inputs:
			return [left_distance, right_distance, up_distance, down_distance]


		# Compare distances
		distances = [(left_distance, 0), (right_distance, 1), (up_distance, 2), (down_distance, 3)]
		distances.sort(key=lambda tup: tup[0], reverse=False)  # Sort in ascending order
		return [i[1] for i in distances]

		# Shuffle directions with same distance values to prevent bias
		# start = 0
		# end = 1
		# for i in range(len(distances)):
		# 	if i < len(distances)-1 and distances[i][0] == distances[i+1][0]:  # if two elements have same distance value
		# 		end += 1
		# 	elif start != end - 1:
		# 		temp = distances[start:end]
		# 		shuffle(temp)
		# 		distances[start:end] = temp
		# 		start = end
		# 		end = start + 1
		#
		# return [i[1] for i in distances]

	@staticmethod
	def check_pellet_on_side(row, col, layout):
		q = []
		q.append(((row, col), 1))  # Add starting point to the queue

		while len(q) != 0: # While queue not empty
			my_tuple = q.pop(0)
			row = my_tuple[0][0]
			col = my_tuple[0][1]
			current_distance = my_tuple[1]

			#TODO yolda canavar varsa napıcagımızı netlestır
			if layout[row][col] == 0:  # If pellet in coordinate, return distance
				return current_distance
			elif layout[row][col] != -1 and layout[row][col] != 1:  # If not visited(-1) and not wall(1) in coordinate, append neighbours to the queue
				# Set visited
				layout[row][col] = -1

				#  Add neighbors to the queue
				q.append(((row, col-1), current_distance+1))  # left
				q.append(((row, col+1), current_distance+1))  # right
				q.append(((row-1, col), current_distance+1))  # up
				q.append(((row+1, col), current_distance+1))  # down

		# If couldn't find pellet, there is no path
		return 1000

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
		pac_left_index = pacman_x - 1
		pac_right_index = pacman_x + 1
		pac_up_index = pacman_y - 1
		pac_down_index = pacman_y + 1
		# print('indecies: ', pac_left_index, pac_right_index, pac_up_index, pac_down_index, pacman_x, pacman_y)

		if pac_left_index >= 0 and self.layout[pacman_y][pac_left_index] == 0:
			pellets[0] = 1
		if pac_right_index <= 18 and self.layout[pacman_y][pac_right_index] == 0:  # we have 19 columns in total
			pellets[1] = 1
		if pac_up_index >= 0 and self.layout[pac_up_index][pacman_x] == 0:
			pellets[2] = 1
		if pac_down_index <= 20 and self.layout[pac_down_index][pacman_x] == 0:  # we have 21 rows in total
			pellets[3] = 1

		return pellets

	def calc_distance_to_closest_ghosts(self, row, col):
		left_layout, right_layout, up_layout, down_layout = self.my_deep_copy(row, col)

		# Calculate distances
		left_distance = self.check_ghost_on_side(row, col-1, left_layout)
		right_distance = self.check_ghost_on_side(row, col+1, right_layout)
		up_distance = self.check_ghost_on_side(row-1, col, up_layout)
		down_distance = self.check_ghost_on_side(row+1, col, down_layout)

		return [left_distance, right_distance, up_distance, down_distance]




	@staticmethod
	def check_ghost_on_side(row, col, layout):
		q = []
		q.append(((row, col), 1))  # Add starting point to the queue

		while len(q) != 0:  # While queue not empty
			my_tuple = q.pop(0)
			row = my_tuple[0][0]
			col = my_tuple[0][1]
			current_distance = my_tuple[1]

			value = layout[row][col]
			if value == 4 or value == 5 or value == 6 or value == 7:  # If ghost in coordinate, return distance
				return 1/current_distance
			elif layout[row][col] != -1 and layout[row][col] != 1:  # If not visited(-1) and not wall(1) in coordinate, append neighbours to the queue
				# Set visited
				layout[row][col] = -1

				#  Add neighbors to the queue
				q.append(((row, col-1), current_distance+1))  # left
				q.append(((row, col+1), current_distance+1))  # right
				q.append(((row-1, col), current_distance+1))  # up
				q.append(((row+1, col), current_distance+1))  # down

		# If couldn't find pellet, there is no path
		return 0

	def my_deep_copy(self, row, col):
		left_layout = deepcopy(self.layout)
		right_layout = deepcopy(self.layout)
		up_layout = deepcopy(self.layout)
		down_layout = deepcopy(self.layout)

		# Set pacman starting position as visited
		left_layout[row][col] = -1
		right_layout[row][col] = -1
		up_layout[row][col] = -1
		down_layout[row][col] = -1

		return left_layout, right_layout, up_layout, down_layout