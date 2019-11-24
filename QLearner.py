from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd


class QLearner:
	ITEMS_TO_REPLAY = 1000

	def __init__(self):
		self.reward = 0
		self.alpha = 0.9
		self.dataframe = pd.DataFrame()
		self.short_memory = np.array([])
		self.agent_target = 1
		self.agent_predict = 0
		self.learning_rate = 0.0005
		self.model = self.create_network()
		self.epsilon = 0
		self.actual = []
		self.memory = []  # Contains information about past decisions.

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
		# 8:  is_closest_to_dot_right
		# 9:  is_closest_to_dot_left
		# 10: is_closest_to_dot_up
		# 11: is_closest_to_dot_down

		walls = map_manager.check_walls(pacman.currentX,pacman.currentY)
		dot_distances = map_manager.get_closest_pellet_direction()

		state = [
			# setting the direction.
			pacman.direction[0],
			pacman.direction[1],
			pacman.direction[2],
			pacman.direction[3],

			# setting the walls.
			walls[0],
			walls[1],
			walls[2],
			walls[3],

			# setting the dot distances.
			dot_distances[0],
			dot_distances[1],
			dot_distances[2],
			dot_distances[3]
		]

		return np.asarray(state)

	def set_reward(self, player):
		self.reward = 0
		if player.is_dead:
			self.reward = -10
			return self.reward

		if player.did_eat:
			self.reward = 10
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