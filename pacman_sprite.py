import basic_sprite
from helpers import *
import level001
import map_manager
import numpy as np

BLOCK_SIZE = 24
x_offset = (BLOCK_SIZE / 2)
y_offset = (BLOCK_SIZE / 2)
level1 = level001.level()
layout = level1.getLayout()[2:]
layout = [row[1:-1] for row in layout]


class Pacman(basic_sprite.Sprite):
	"""This is our snake that will move around the screen"""

	def __init__(self, centerPoint, image, map_manager: map_manager, speed):
		basic_sprite.Sprite.__init__(self, centerPoint, image)
		"""Initialize the number of pellets eaten"""
		self.pellets = 0
		self.did_eat = False
		self.is_dead = False
		"""Set the number of Pixels to move each time"""
		self.speed = speed

		# """Initialize how much we are moving"""
		self.xMove = 0
		self.yMove = 0

		self.score = 0

		self.direction = [0, 0, 0, 0]
		self.nextdir = [0, 0, 0, 0]
		# self.xdir = [0, -self.dist, self.dist, 0, 0]
		# self.ydir = [0, 0, 0, -self.dist, self.dist]

		# Coordinates in tile format.
		# X increases in East direction.
		# Y increses in South direction.
		self.currentX = 9
		self.currentY = 15
		self.tile_x = 9
		self.tile_y = 15
		# layout[self.currentY][self.currentX] = 9

		self.map_manager = map_manager
		self.is_next_dir_performed = True
		self.did_change_tile = True

	def get_direction(self):
		return self.direction


	def move_key_down(self, key):
		"""This function sets the xMove or yMove variables that will
        then move the snake when update() function is called.  The
        xMove and yMove values will be returned to normal when this 
        keys MoveKeyUp function is called."""

		#self.direction = self.nextdir

		if (key == K_RIGHT):
			self.nextdir = [0, 1, 0, 0]
		elif (key == K_LEFT):
			self.nextdir = [1, 0, 0, 0]
		elif (key == K_UP):
			self.nextdir = [0, 0, 1, 0]
		elif (key == K_DOWN):
			self.nextdir = [0, 0, 0, 1]

		self.is_next_dir_performed = False

	def do_move(self, direction):
		self.nextdir = direction
		self.is_next_dir_performed = False


	def update(self, block_group):
		"""Called when the Snake sprite should update itself"""

		# Going left or right
		if self.direction[0] == 1 or self.direction[1] == 1:
			# if(self.rect.centerx-36) % 24 == 0:
			self.tile_x = round((self.rect.centerx - 36)/BLOCK_SIZE)

		# Going up or down
		if self.direction[2] == 1 or self.direction[3] == 1:
			# if ((self.rect.centery - 60) % 24 == 0):
			self.tile_y = round((self.rect.centery - 60) / BLOCK_SIZE )

		# if location is changed.
		if self.tile_x != self.currentX or self.tile_y != self.currentY:

			#print("new Tile")
			self.map_manager.move_pacman(self.tile_x, self.tile_y,self)
			self.currentX = self.tile_x
			self.currentY = self.tile_y
			self.did_change_tile = True
		else:
			self.did_change_tile = False

		walls = self.map_manager.check_walls(self.tile_x, self.tile_y)
		wall_in_next_dir = np.add(np.asarray(walls), np.asarray(self.nextdir))
		wall_in_curr_dir = np.add(np.asarray(walls), np.asarray(self.direction))

		new_result = np.where(wall_in_next_dir == 2)
		old_result = np.where(wall_in_curr_dir == 2)
		# I can move to next_dir
		if not self.is_next_dir_performed and np.asarray(new_result).size == 0 and ((self.rect.centery - 12) % 24 == 0) and ((self.rect.centerx - 12) % 24 == 0):
			# calculates move depending on next_dir array.
			self.xMove = ((self.nextdir[0] * -1) + (self.nextdir[1])) * self.speed
			self.yMove = ((self.nextdir[2] * -1) + (self.nextdir[3])) * self.speed
			self.rect.move_ip(self.xMove, self.yMove)
			if not np.array_equal( self.nextdir, self.direction):
				self.direction = self.nextdir
			self.is_next_dir_performed = True
			#print('next_dir')

		# I can continue on my old direction.
		elif np.asarray(old_result).size == 0 or not ((self.rect.centery - 12) % 24 == 0 and (self.rect.centerx - 12) % 24 == 0):
				self.rect.move_ip(self.xMove, self.yMove)
			#print('old_dir')
		# I cannot move anywhere otherwise.
		elif ((self.rect.centery - 12) % 24 == 0) and ((self.rect.centerx - 12) % 24 == 0):
			self.xMove = 0
			self.yMove = 0
			self.rect.move_ip(self.xMove, self.yMove)
			#print('stop')





		# self.rect.move_ip(self.xMove, self.yMove)
		#
		# """IF we hit a block, don't move - reverse the movement"""
		# if pygame.sprite.spritecollide(self, block_group, False):
		# 	self.rect.move_ip(-self.xMove, -self.yMove)
		# 	"""IF we can't move in the new direction... continue in old direction"""
		# 	self.xMove = self.xdir[self.direction]
		# 	self.yMove = self.ydir[self.direction]
		# 	self.rect.move_ip(self.xMove, self.yMove)
		#
		# 	if pygame.sprite.spritecollide(self, block_group, False):
		# 		self.rect.move_ip(-self.xMove, -self.yMove)
		# 		self.yMove = 0
		# 		self.xMove = 0
		# 		self.direction = 0
		# 		self.nextdir = 0
		# else:
		# 	self.direction = 0


class Ghost(basic_sprite.Sprite):
	"""This is our ghost that will move around the screen"""

	def __init__(self, centerPoint, image):

		basic_sprite.Sprite.__init__(self, centerPoint, image)
		"""Initialize the number of pellets eaten"""
		self.pellets = 0
		"""Set the number of Pixels to move each time"""
		self.dist = 2

		"""Initialize how much we are moving"""
		self.xMove = 0
		self.yMove = 0

		self.direction = 1
		self.nextdir = 3
		self.xdir = [0, -self.dist, self.dist, 0, 0]
		self.ydir = [0, 0, 0, -self.dist, self.dist]

	def update(self, block_group):
		"""Called when the Ghost sprit should update itself"""
		# print self.nextdir,self.direction
		#
		# self.xMove = self.xdir[self.nextdir]
		# self.yMove = self.ydir[self.nextdir]
		#
		# self.rect.move_ip(self.xMove, self.yMove)
		#
		# if pygame.sprite.spritecollide(self, block_group, False):
		# 	self.rect.move_ip(-self.xMove, -self.yMove)
		#
		# 	self.xMove = self.xdir[self.direction]
		# 	self.yMove = self.ydir[self.direction]
		# 	self.rect.move_ip(self.xMove, self.yMove)
		#
		# 	if pygame.sprite.spritecollide(self, block_group, False):
		# 		self.rect.move_ip(-self.xMove, -self.yMove)
		# 		if self.nextdir < 3:
		# 			self.nextdir = randint(3, 4)
		# 		else:
		# 			self.nextdir = randint(1, 2)
		# else:
		# 	self.direction = self.nextdir
		# 	if self.nextdir < 3:
		# 		self.nextdir = randint(3, 4)
		# 	else:
		# 		self.nextdir = randint(1, 2)
