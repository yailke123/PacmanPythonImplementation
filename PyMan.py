from keras.utils import to_categorical

import level001
import basicSprite
from helpers import *
from snakeSprite import Pacman, Ghost
from image import *
import QLearner
import MapManager
from random import randint
import numpy as np
import time
import seaborn as sns
import matplotlib.pyplot as plt




# TODO
# > add power pills
# > add quit option
# > improve sound substructure
# > add better object code and polymorphism
# > add cherries etc / powerups
# > choose control of ghost / pacman
# > option submenu


clock = pygame.time.Clock()

if not pygame.font:
	print('Warning, fonts disabled')
# if not pygame.mixer:
# 	print('Warning, sound disabled')

BLOCK_SIZE = 24
IS_AI = True

def plot_seaborn(array_counter, array_score):
    sns.set(color_codes=True)
    ax = sns.regplot(np.array([array_counter])[0], np.array([array_score])[0], color="b", x_jitter=.1, line_kws={'color':'green'})
    ax.set(xlabel='games', ylabel='score')
    plt.show()

class PyManMain:
	"""The Main PyMan Class - This class handles the main
    initialization and creating of the Game."""

	def __init__(self, width=640, height=480):
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
		self.isGameOver = False
		print("alo ")
		# Setup the variables
		# TODO: understand
		self.collisiontol = 5
		self.collisions = 0

		self.initial_layout = level001.level().getLayout()
		self.learner = QLearner.QLearner()
		self.map_manager = MapManager.MapManager(self.initial_layout)
		self.pacman = None
		self.game_counter = 0
		self.score = 0
		self.record = 0

	def get_record(self, score, record):
		if score >= record:
			return score
		else:
			return record





	def main_loop(self):
		score_plot = []
		counter_plot = []
		"""This is the Main Loop of the Game"""
		while 1:
			"""Load All of our Sprites"""
			self.LoadSprites()

			"""Create the background"""
			self.background = pygame.Surface(self.screen.get_size())
			self.background = self.background.convert()
			self.background.fill((0, 0, 0))
			"""Draw the blocks onto the background, since they only need to be drawn once"""
			self.block_sprites.draw(self.background)
			self.gwall_sprites.draw(self.background)

			while 1:
				if not IS_AI:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()
						elif event.type == KEYDOWN:  # or event.type == KEYUP
							if ((event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP)
									or (event.key == K_DOWN)):
								self.pacman.MoveKeyDown(event.key)
				# #self.pacman_sprites.update(self.block_sprites)
				#
				# # Not rendering ghost for now.
				# # TODO: Render Ghosts.
				# # self.ghost_sprites.update(self.block_sprites)
				# # self.ghost2_sprites.update(self.block_sprites)
				# # self.ghost3_sprites.update(self.block_sprites)
				# # self.ghost4_sprites.update(self.block_sprites)
				#
				# if not (not pygame.sprite.collide_rect(self.ghost, self.pacman) and not pygame.sprite.collide_rect(
				# 		self.ghost2,
				# 		self.pacman)) or pygame.sprite.collide_rect(
				# 	self.ghost3, self.pacman) or pygame.sprite.collide_rect(self.ghost4, self.pacman):
				# 	self.collisions += 1
				# 	print("Col+1", self.collisions)
				# 	if self.collisions == self.collisiontol:
				# 		self.game_counter += 1
				# 		self.isGameOver = True
				# 		print("gameover", self.game_counter)
				# 		if IS_AI:
				# 			self.learner.replay_new(self.learner.memory)
				# 		break
				# else:
				# 	self.collisions = 0
				#
				# """Check for a snake collision/pellet collision"""
				# lstCols = pygame.sprite.spritecollide(self.pacman, self.pellet_sprites, True)
				# """Update the amount of pellets eaten"""
				# self.pacman.pellets = self.pacman.pellets + len(lstCols)
				# self.score = self.pacman.pellets * 10
				#
				#
				# """Do the Drawing"""
				# self.screen.blit(self.background, (0, 0))
				# if pygame.font:
				# 	font = pygame.font.Font(None, 36)
				# 	text = font.render("Score %s" % self.score, 1, (255, 255, 255))
				# 	textpos = text.get_rect(x=0)
				# 	self.screen.blit(text, textpos)
				#
				# self.pellet_sprites.draw(self.screen)
				# self.pacman_sprites.draw(self.screen)
				# self.ghost_sprites.draw(self.screen)
				# self.ghost2_sprites.draw(self.screen)
				# self.ghost3_sprites.draw(self.screen)
				# self.ghost4_sprites.draw(self.screen)
				# pygame.display.flip()
				# clock.tick(40)
				else:
					if self.game_counter < 25 and not self.isGameOver:
						self.end = time.time()
						self.elapsed_time = self.end-self.start
						if(self.elapsed_time > 5):
							print("sure biti")
							self.start = time.time()
							counter_plot.append(self.game_counter)
							score_plot.append(self.score)
							self.game_counter += 1
							self.isGameOver = True
							break
						print(self.end-self.start)
						print("baslıyoruz kızlar")
						self.learner.epsilon = 60 - self.game_counter
						old_state = self.learner.get_state(self.map_manager, self.pacman)
						print("basladık")
						if randint(0, 200) <self.learner.epsilon:
							final_move = to_categorical(randint(0, 2), num_classes=4)
						else:
							# predict action based on the old state
							prediction = self.learner.model.predict(old_state.reshape((1, 12)))
							final_move = to_categorical(np.argmax(prediction[0]), num_classes=4)
							print('mydecision: ', final_move)
						# perform new move and get new state
						self.pacman.do_move(final_move)
						state_new = self.learner.get_state(self.map_manager, self.pacman)

						# set reward for the new state
						reward = self.learner.set_reward(self.pacman)
						# train short memory base on the new action and state
						self.learner.train_short_memory(old_state, final_move, reward, state_new, self.isGameOver)

						# store the new data into a long term memory
						self.learner.remember(old_state, final_move, reward, state_new, self.isGameOver)
						self.record = self.get_record(self.score, self.record)

						#EGENIN BOS ISLERI SOVU BASLIYORU
						if not (not pygame.sprite.collide_rect(self.ghost, self.pacman) and not pygame.sprite.collide_rect(
								self.ghost2,
								self.pacman)) or pygame.sprite.collide_rect(
							self.ghost3, self.pacman) or pygame.sprite.collide_rect(self.ghost4, self.pacman):
							self.collisions += 1
							print("Col+1", self.collisions)
							if self.collisions == self.collisiontol:
								self.game_counter += 1
								self.isGameOver = True
								print("gameover", self.game_counter)
								if IS_AI:
									self.learner.replay_new(self.learner.memory)
								break
						else:
							self.collisions = 0

						"""Check for a snake collision/pellet collision"""
						lstCols = pygame.sprite.spritecollide(self.pacman, self.pellet_sprites, True)
						"""Update the amount of pellets eaten"""
						self.pacman.pellets = self.pacman.pellets + len(lstCols)
						self.score = self.pacman.pellets * 10

						"""Do the Drawing"""
						self.screen.blit(self.background, (0, 0))
						if pygame.font:
							font = pygame.font.Font(None, 36)
							text = font.render("Score %s" % self.score, 1, (255, 255, 255))
							textpos = text.get_rect(x=0)
							self.screen.blit(text, textpos)

						self.pellet_sprites.draw(self.screen)
						self.pacman_sprites.draw(self.screen)
						self.ghost_sprites.draw(self.screen)
						self.ghost2_sprites.draw(self.screen)
						self.ghost3_sprites.draw(self.screen)
						self.ghost4_sprites.draw(self.screen)
						pygame.display.flip()
						clock.tick(40)
						#EGENIN BOS ISLERI SOVU BITI

				print("buraya geldıysen serefsızsın")
				self.pacman_sprites.update(self.block_sprites)
				self.isGameOver = False

				if (self.game_counter >= 25):
					plot_seaborn(counter_plot, score_plot)
				"""Update the sprites"""
				# #self.pacman_sprites.update(self.block_sprites)
				#
				# # Not rendering ghost for now.
				# # TODO: Render Ghosts.
				# # self.ghost_sprites.update(self.block_sprites)
				# # self.ghost2_sprites.update(self.block_sprites)
				# # self.ghost3_sprites.update(self.block_sprites)
				# # self.ghost4_sprites.update(self.block_sprites)
				#
				# if not (not pygame.sprite.collide_rect(self.ghost, self.pacman) and not pygame.sprite.collide_rect(
				# 		self.ghost2,
				# 		self.pacman)) or pygame.sprite.collide_rect(
				# 	self.ghost3, self.pacman) or pygame.sprite.collide_rect(self.ghost4, self.pacman):
				# 	self.collisions += 1
				# 	print("Col+1", self.collisions)
				# 	if self.collisions == self.collisiontol:
				# 		self.game_counter += 1
				# 		self.isGameOver = True
				# 		print("gameover", self.game_counter)
				# 		if IS_AI:
				# 			self.learner.replay_new(self.learner.memory)
				# 		break
				# else:
				# 	self.collisions = 0
				#
				# """Check for a snake collision/pellet collision"""
				# lstCols = pygame.sprite.spritecollide(self.pacman, self.pellet_sprites, True)
				# """Update the amount of pellets eaten"""
				# self.pacman.pellets = self.pacman.pellets + len(lstCols)
				# self.score = self.pacman.pellets * 10
				#
				#
				# """Do the Drawing"""
				# self.screen.blit(self.background, (0, 0))
				# if pygame.font:
				# 	font = pygame.font.Font(None, 36)
				# 	text = font.render("Score %s" % self.score, 1, (255, 255, 255))
				# 	textpos = text.get_rect(x=0)
				# 	self.screen.blit(text, textpos)
				#
				# self.pellet_sprites.draw(self.screen)
				# self.pacman_sprites.draw(self.screen)
				# self.ghost_sprites.draw(self.screen)
				# self.ghost2_sprites.draw(self.screen)
				# self.ghost3_sprites.draw(self.screen)
				# self.ghost4_sprites.draw(self.screen)
				# pygame.display.flip()
				# clock.tick(40)
			# print clock.get_fps()
			# self.sounds['die'].play()

	def LoadSprites(self):
		"""Load all of the sprites that we need"""
		"""calculate the center point offset"""
		x_offset = (BLOCK_SIZE / 2)
		y_offset = (BLOCK_SIZE / 2)
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
				centerPoint = [(x * BLOCK_SIZE) + x_offset, (y * BLOCK_SIZE + y_offset)]
				# print centerPoint
				if self.initial_layout[y][x] == level1.BLOCK:
					self.block_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.BLOCK]))
				elif self.initial_layout[y][x] == level1.GWALL:
					self.gwall_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.GWALL]))
				elif self.initial_layout[y][x] == level1.SNAKE:
					self.pacman = Pacman(centerPoint, img_list[level1.SNAKE], self.map_manager)
				elif self.initial_layout[y][x] == level1.PELLET:
					self.pellet_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.PELLET]))
				elif self.initial_layout[y][x] == level1.GHOST:
					self.ghost = Ghost(centerPoint, img_list[level1.GHOST])
				elif self.initial_layout[y][x] == level1.GHOST2:
					self.ghost2 = Ghost(centerPoint, img_list[level1.GHOST2])
				elif self.initial_layout[y][x] == level1.GHOST3:
					self.ghost3 = Ghost(centerPoint, img_list[level1.GHOST3])
				elif self.initial_layout[y][x] == level1.GHOST4:
					self.ghost4 = Ghost(centerPoint, img_list[level1.GHOST4])

		"""Create the Snake group"""
		self.pacman_sprites = pygame.sprite.RenderPlain(self.pacman)
		self.ghost_sprites = pygame.sprite.RenderPlain(self.ghost)
		self.ghost2_sprites = pygame.sprite.RenderPlain(self.ghost2)
		self.ghost3_sprites = pygame.sprite.RenderPlain(self.ghost3)
		self.ghost4_sprites = pygame.sprite.RenderPlain(self.ghost4)

		# self.player = Player(self.pacman)


if __name__ == "__main__":
	MainWindow = PyManMain(500, 575)
	MainWindow.main_loop()
