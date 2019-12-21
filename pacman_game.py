from keras.utils import to_categorical
import level001
import basic_sprite
from helpers import *
from pacman_sprite import Pacman, Ghost
from image import *
import q_learner
import map_manager
from random import randint
import numpy as np
import time
import seaborn as sns
import matplotlib.pyplot as plt
import sys


def plot_seaborn(array_counter, array_score):
	sns.set(color_codes=True)
	ax = sns.regplot(np.array([array_counter])[0], np.array([array_score])[0], color="b", x_jitter=.1,
	                 line_kws={'color': 'green'})
	ax.set(xlabel='games', ylabel='score')
	plt.show()


class PyManMain:
	"""The Main PyMan Class - This class handles the main
	initialization and creating of the Game."""
	BLOCK_SIZE = 24

	IS_AI = True
	FPS = 240
	NUMBER_OF_GAMES_TO_TRAIN = 50
	GENERATION_TIMER = 15
	INITIAL_EPSILON = 40
	RAND_UPPER_BOUND = 80
	PACMAN_SPEED = 3
	DECISION_TIMEOUT_CONSTANT = 2

	def __init__(self, width=640, height=480):
		if os.path.isfile('weights.hdf5'):
			#self.INITIAL_EPSILON = 0
			pass
		"""Initialize"""
		pygame.init()
		self.start = time.time()
		self.end = time.time()
		self.elapsed_time = 0

		"""Set the window Size"""
		self.width = width
		self.height = height

		"""Create the Screen"""
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("AI playing PacMan in style!")

		self.is_game_over = False
		self.initial_layout = level001.level().getLayout()
		self.learner = q_learner.QLearner()
		self.map_manager = map_manager.MapManager(self.initial_layout)
		self.pacman = None
		self.game_counter = 0
		self.score = 0
		self.record = 0
		self.frame_count_since_last_decision = 0
		self.frame_count_threshold = self.BLOCK_SIZE / self.PACMAN_SPEED * self.DECISION_TIMEOUT_CONSTANT

	def get_record(self, score, record):
		if score >= record:
			return score
		else:
			return record

	def hit_by_ghost(self):
		return pygame.sprite.collide_rect(self.ghost, self.pacman) or \
				pygame.sprite.collide_rect(self.ghost2, self.pacman) or \
				pygame.sprite.collide_rect(self.ghost3, self.pacman) or \
				pygame.sprite.collide_rect(self.ghost4, self.pacman)


	def update_score(self):
		collide_list = pygame.sprite.spritecollide(self.pacman, self.pellet_sprites, True)
		"""Update the amount of pellets eaten"""
		self.pacman.pellets = self.pacman.pellets + len(collide_list)
		self.score = self.pacman.pellets * 10

	def draw_objects(self):
		self.screen.blit(self.background, (0, 0))
		if pygame.font:
			font = pygame.font.SysFont("sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic", 19)
			text = font.render("Score: %s" % self.score, 1, (235, 49, 201))
			textpos = text.get_rect(x=0)
			self.screen.blit(text, textpos)

			text = font.render("Game Count: %s" % self.game_counter, 1, (66, 245, 114))
			textpos = text.get_rect(x=125)
			self.screen.blit(text, textpos)

			text = font.render("Random Prob: %s%%" % round((self.learner.epsilon / self.RAND_UPPER_BOUND)*100), 1, (66, 135, 245))
			textpos = text.get_rect(x=290)
			self.screen.blit(text, textpos)

		self.pellet_sprites.draw(self.screen)
		self.pacman_sprites.draw(self.screen)
		self.ghost_sprites.draw(self.screen)
		self.ghost2_sprites.draw(self.screen)
		self.ghost3_sprites.draw(self.screen)
		self.ghost4_sprites.draw(self.screen)
		pygame.display.flip()
		clock.tick(self.FPS)

	def update_ghosts(self):
		self.ghost_sprites.update(self.block_sprites)
		self.ghost2_sprites.update(self.block_sprites)
		self.ghost3_sprites.update(self.block_sprites)
		self.ghost4_sprites.update(self.block_sprites)

	def reset_game(self):
		self.load_sprites()
		self.draw_static_objects()
		self.map_manager.reset_map(self.initial_layout)
		self.learner.epsilon = self.INITIAL_EPSILON - self.game_counter
		self.pacman.did_change_tile = True
		self.pacman.is_dead = False
		self.is_game_over = False
		self.frame_count_since_last_decision = 0
		self.start = time.time()

	def draw_static_objects(self):
		"""Create the background"""
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))
		"""Draw the blocks onto the background, since they only need to be drawn once"""
		self.block_sprites.draw(self.background)
		self.gwall_sprites.draw(self.background)

	def load_sprites(self):
		"""Load all of the sprites that we need"""
		"""calculate the center point offset"""
		x_offset = (self.BLOCK_SIZE / 2)
		y_offset = (self.BLOCK_SIZE / 2)
		"""Load the level"""
		level1 = level001.level()
		# layout = level1.getLayout()
		img_list = level1.getSprites()

		self.pellet_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.gwall_sprites = pygame.sprite.Group()

		for y in range(len(self.initial_layout)):
			for x in range(len(self.initial_layout[y])):
				"""Get the center point for the rects"""
				centerPoint = [(x * self.BLOCK_SIZE) + x_offset, (y * self.BLOCK_SIZE + y_offset)]
				# print centerPoint
				if self.initial_layout[y][x] == level1.BLOCK:
					self.block_sprites.add(basic_sprite.Sprite(centerPoint, img_list[level1.BLOCK]))
				elif self.initial_layout[y][x] == level1.GWALL:
					self.gwall_sprites.add(basic_sprite.Sprite(centerPoint, img_list[level1.GWALL]))
				elif self.initial_layout[y][x] == level1.SNAKE:
					self.pacman = Pacman(centerPoint, img_list[level1.SNAKE], self.map_manager, self.PACMAN_SPEED)
				elif self.initial_layout[y][x] == level1.PELLET:
					self.pellet_sprites.add(basic_sprite.Sprite(centerPoint, img_list[level1.PELLET]))
				elif self.initial_layout[y][x] == level1.GHOST:
					self.ghost = Ghost(centerPoint, img_list[level1.GHOST])
				elif self.initial_layout[y][x] == level1.GHOST2:
					self.ghost2 = Ghost(centerPoint, img_list[level1.GHOST2])
				elif self.initial_layout[y][x] == level1.GHOST3:
					self.ghost3 = Ghost(centerPoint, img_list[level1.GHOST3])
				elif self.initial_layout[y][x] == level1.GHOST4:
					self.ghost4 = Ghost(centerPoint, img_list[level1.GHOST4])

		self.pacman_sprites = pygame.sprite.RenderPlain(self.pacman)
		self.ghost_sprites = pygame.sprite.RenderPlain(self.ghost)
		self.ghost2_sprites = pygame.sprite.RenderPlain(self.ghost2)
		self.ghost3_sprites = pygame.sprite.RenderPlain(self.ghost3)
		self.ghost4_sprites = pygame.sprite.RenderPlain(self.ghost4)

	def main_loop(self):
		score_plot = []
		counter_plot = []

		# Infinitely many games generated.

		while self.game_counter < self.NUMBER_OF_GAMES_TO_TRAIN:
			self.game_counter += 1
			# Sets game to its initial state.
			self.reset_game()
			# if self.game_counter > self.NUMBER_OF_GAMES_TO_TRAIN:
			# 	plot_seaborn(counter_plot, score_plot)
			# 	self.learner.save_weights_h5()
			# Give infinite inputs for the game.
			while not self.is_game_over:
				# Player is playing
				if not self.IS_AI:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()
						elif event.type == KEYDOWN:  # or event.type == KEYUP
							if ((event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP)
									or (event.key == K_DOWN)):
								self.pacman.move_key_down(event.key)

					# Check if collided.
					if self.hit_by_ghost():
						self.is_game_over = True

				# AI is playing.
				else:
					# Game is still on
					if self.game_counter <= self.NUMBER_OF_GAMES_TO_TRAIN and not self.is_game_over:
						self.end = time.time()
						self.elapsed_time = self.end - self.start
						self.frame_count_since_last_decision += 1

						# Game is timed-out.
						if self.elapsed_time > self.GENERATION_TIMER:
							counter_plot.append(self.game_counter)
							score_plot.append(self.score)
							self.is_game_over = True

						elif self.pacman.did_change_tile or self.frame_count_since_last_decision > self.frame_count_threshold:
							if self.frame_count_since_last_decision > self.frame_count_threshold:
								self.pacman.did_eat = False
							old_state = self.learner.get_state(self.map_manager, self.pacman)
							if randint(0, self.RAND_UPPER_BOUND) < self.learner.epsilon:
								final_move = to_categorical(randint(0, 3), num_classes=4)
								# print('Random move: ', final_move)
							else:
								# predict action based on the old state
								prediction = self.learner.model.predict(old_state.reshape((1, 12)))
								final_move = to_categorical(np.argmax(prediction[0]), num_classes=4)
								# print('Neural move: ', final_move)

							# perform new move and get new state
							self.pacman.do_move(final_move)

							if self.hit_by_ghost():
								self.is_game_over = True
								self.pacman.is_dead = True

							state_new = self.learner.get_state(self.map_manager, self.pacman)

							# set reward for the new state
							reward = self.learner.set_reward(self.pacman, self.frame_count_since_last_decision)

							# train short memory base on the new action and state
							self.learner.train_short_memory(old_state, final_move, reward, state_new, self.is_game_over)

							# store the new data into a long term memory
							self.learner.remember(old_state, final_move, reward, state_new, self.is_game_over)
							self.record = self.get_record(self.score, self.record)

							self.frame_count_since_last_decision = 0

						if self.is_game_over:
							self.learner.replay_new(self.learner.memory)

				# Both AI and Player
				# Draw after input
				self.pacman_sprites.update(self.block_sprites)
				# self.update_ghosts()
				self.update_score()
				self.draw_objects()


		# At the end of each game.
		# if self.game_counter >= self.NUMBER_OF_GAMES_TO_TRAIN:
		plot_seaborn(counter_plot, score_plot)
		self.learner.save_weights_h5()

if __name__ == "__main__":
	clock = pygame.time.Clock()

	if not pygame.font:
		print('Warning, fonts disabled')
	MainWindow = PyManMain(500, 575)
	MainWindow.main_loop()
