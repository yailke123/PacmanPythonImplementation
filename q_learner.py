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

	def __init__(self):
		self.reward = 0
		self.alpha = 0.1
		self.dataframe = pd.DataFrame()
		self.short_memory = np.array([])
		self.agent_target = 1
		self.agent_predict = 0
		self.learning_rate = 0.0005

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
		# 8:
		# 9:
		# 10:
		# 11:

		walls = map_manager.check_walls(pacman.currentX, pacman.currentY)
		# dot_distances = map_manager.get_closest_pellet_direction(pacman.currentX, pacman.currentY)
		closest_directions = map_manager.calc_distance_to_closest_pellets(pacman.currentY, pacman.currentX) # TODO x y doru mu emin ol
		# ghost_directions = map_manager.calc_distance_to_closest_ghosts(pacman.currentY, pacman.currentX)
		ghost_directions = [0, 0, 0, 0]
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

			#ghosts
			ghost_directions[0],  # 1/left_distance
			ghost_directions[1],  # 1/right_distance
			ghost_directions[2],
			ghost_directions[3]
		]

		return np.asarray(state)

	def set_reward(self, player, frame_count):
		self.reward = 0
		time_penalty = int(frame_count * self.FRAME_PENALIZE_COEFFICIENT)
		if player.is_dead:
			self.reward = -71
			return self.reward
		if player.did_eat:
			self.reward = 10
		self.reward -= time_penalty
		return self.reward

	def create_network(self, weights=None):
		model = Sequential()
		model.add(Dense(activation="relu", input_dim=12, units=120))
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
			target = reward + self.alpha * np.amax(self.model.predict(next_state.reshape((1, 12)))[0])
		target_f = self.model.predict(state.reshape((1, 12)))
		target_f[0][np.argmax(action)] = target
		self.model.fit(state.reshape((1, 12)), target_f, epochs=1, verbose=0)

	def save_weights_h5(self):
		self.model.save("weights.hdf5")
