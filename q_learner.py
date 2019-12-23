from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
import os.path
import h5py


class QLearner:
	ITEMS_TO_REPLAY = 1000
	FRAME_PENALIZE_COEFFICIENT = 0.3
	NN_INPUT_SIZE = 21

	def __init__(self):
		self.reward = 0
		self.alpha = 0.1
		self.dataframe = pd.DataFrame()
		self.short_memory = np.array([])
		self.agent_target = 1
		self.agent_predict = 0
		self.learning_rate = 0.0007

		if os.path.isfile('weights.hdf5'):
			self.model = self.create_network("weights.hdf5")
		else:
			self.model = self.create_network()

		self.actual = []
		self.memory = []  # Contains information about past decisions.
		self.epsilon = 0

	def get_state(self, map_manager, pacman):
		# Returns array with 12  entries. Entries correspond to:
		# 0:  is_moving_left
		# 1:  is_moving_right
		# 2:  is_moving_up
		# 3:  is_moving_down
		# 4:  can_move_left
		# 5:  can_move_right
		# 6:  can_move_up
		# 7:  can_move_down
		# 8:  is_closest_to_dot_left
		# 9:  is_closest_to_dot_right
		# 10: is_closest_to_dot_up
		# 11: is_closest_to_dot_down

		# if is_future_move:
		# 	x = pacman.currentX - pacman.nextdir[0] + pacman.nextdir[1]
		# 	y = pacman.currentY - pacman.nextdir[2] + pacman.nextdir[3]
		# 	x = int(x)
		# 	y = int(y)
		#
		# 	if map_manager.layout[y][x] == 1:
		# 		x = pacman.currentX
		# 		y = pacman.currentY
		# else:
		# 	x = pacman.currentX
		# 	y = pacman.currentY
		#
		# x = int(x)
		# y = int(y)

		x = pacman.currentX
		y = pacman.currentY
		x = int(x)
		y = int(y)

		walls = map_manager.check_walls(x, y)
		# dot_distances = map_manager.get_closest_pellet_direction(x, y)
		closest_directions, pellet_distance_values = map_manager.calc_distance_to_closest_pellets(y, x)  # TODO x y doru mu emin ol
		# ghost = [0,0,0,0]
		ghost_distances = map_manager.check_ghost(y, x)

		can_focus_on_eating = 0
		if 1 not in ghost_distances:
			for value in pellet_distance_values:
				if value < 3:
					can_focus_on_eating = 1
		# print(ghost_distances)

		dead = pacman.is_dead
		state = [
			# setting the walls.
			walls[0],
			walls[1],
			walls[2],
			walls[3],

			# left uzaklıkta kacıncı sırada vs
			closest_directions.index(0),
			closest_directions.index(1),
			closest_directions.index(2),
			closest_directions.index(3),

			ghost_distances[0],
			ghost_distances[1],
			ghost_distances[2],
			ghost_distances[3],
			ghost_distances[4],
			ghost_distances[5],
			ghost_distances[6],
			ghost_distances[7],
			ghost_distances[8],
			ghost_distances[9],
			ghost_distances[10],
			ghost_distances[11],
			# can_focus_on_eating

			dead

			# ghost_distances.index(0),
			# ghost_distances.index(1),
			# ghost_distances.index(2),
			# ghost_distances.index(3)

		]
		return np.asarray(state)

	def set_reward(self, player, frame_count):
		self.reward = 0
		time_penalty = int(frame_count * self.FRAME_PENALIZE_COEFFICIENT)
		if player.is_dead:
			self.reward = -250
			print('Reward', self.reward)
			return self.reward
		if player.did_eat:
			self.reward = 10
		self.reward -= time_penalty
		print('Reward', self.reward)
		return self.reward


	def create_network(self, weights=None):
		model = Sequential()
		model.add(Dense(activation="relu", input_dim=self.NN_INPUT_SIZE, units=120))
		model.add(Dropout(0.15))
		model.add(Dense(activation="relu", units=120))
		model.add(Dropout(0.15))
		model.add(Dense(activation="relu", units=120))
		model.add(Dropout(0.15))
		model.add(Dense(activation='softmax', units=4))
		opt = Adam(self.learning_rate)
		model.compile(loss='mse', optimizer=opt)

		if weights:
			model.load_weights(weights)
		return model

	def remember(self, state, action, reward, next_state, is_dead):
		self.memory.append((state, action, reward, next_state, is_dead))

	def replay_new(self, memory):
		# Limiting the number of items to fetch from memory.
		if len(memory) > self.ITEMS_TO_REPLAY:
			# Takes ITEMS_TO_REPLAY random items from the memory.
			batch = random.sample(memory, self.ITEMS_TO_REPLAY)
		else:
			batch = memory

		for state, action, reward, next_state, is_dead in batch:
			target = reward
			if not is_dead:
				target = reward + self.alpha * np.amax(self.model.predict(np.array([next_state]))[0])
			target_f = self.model.predict(np.array([state]))
			target_f[0][np.argmax(action)] = target
			self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

	def train_short_memory(self, state, action, reward, next_state, is_dead):
		target = reward
		if not is_dead:
			target = reward + self.alpha * np.amax(self.model.predict(next_state.reshape((1, self.NN_INPUT_SIZE)))[0])
		target_f = self.model.predict(state.reshape((1, self.NN_INPUT_SIZE)))
		target_f[0][np.argmax(action)] = target
		self.model.fit(state.reshape((1, self.NN_INPUT_SIZE)), target_f, epochs=1, verbose=0)

	def save_weights_h5(self):
		self.model.save("weights.hdf5")
