import basicSprite
from helpers import *
import level001
import MapManager

BLOCK_SIZE = 24
x_offset = (BLOCK_SIZE / 2)
y_offset = (BLOCK_SIZE / 2)
level1 = level001.level()
layout = level1.getLayout()[2:]
layout = [row[1:-1] for row in layout]


class Pacman(basicSprite.Sprite):
	"""This is our snake that will move around the screen"""

	def __init__(self, centerPoint, image, map_manager: MapManager):
		basicSprite.Sprite.__init__(self, centerPoint, image)
		"""Initialize the number of pellets eaten"""
		self.pellets = 0
		"""Set the number of Pixels to move each time"""
		self.speed = 3

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

		# layout[self.currentY][self.currentX] = 9

		self.map_manager = map_manager

	def get_direction(self):
		return self.direction

	def MoveKeyDown(self, key):
		"""This function sets the xMove or yMove variables that will
        then move the snake when update() function is called.  The
        xMove and yMove values will be returned to normal when this 
        keys MoveKeyUp function is called."""

		self.direction = self.nextdir

		if (key == K_RIGHT):
			self.nextdir = [0, 1, 0, 0]
		elif (key == K_LEFT):
			self.nextdir = [1, 0, 0, 0]
		elif (key == K_UP):
			self.nextdir = [0, 0, 1, 0]
		elif (key == K_DOWN):
			self.nextdir = [0, 0, 0, 1]

	def update(self, block_group):
		"""Called when the Snake sprit should update itself"""
		# calculates move depending on next_dir array.
		self.xMove = ((self.nextdir[0] * -1) + (self.nextdir[1])) * self.speed
		self.yMove = ((self.nextdir[2] * -1) + (self.nextdir[3])) * self.speed

		tile_x = int((self.rect.left - x_offset)/BLOCK_SIZE)
		tile_y = int((self.rect.top - y_offset)/BLOCK_SIZE - 1)

		# if location is changed.
		if tile_x != self.currentX or tile_y != self.currentY:
			self.map_manager.move_pacman(tile_x, tile_y)
			self.currentX = tile_x
			self.currentY = tile_y

		self.rect.move_ip(self.xMove, self.yMove)

		"""IF we hit a block, don't move - reverse the movement"""
		if pygame.sprite.spritecollide(self, block_group, False):
			self.rect.move_ip(-self.xMove, -self.yMove)
			"""IF we can't move in the new direction... continue in old direction"""
			self.xMove = self.xdir[self.direction]
			self.yMove = self.ydir[self.direction]
			self.rect.move_ip(self.xMove, self.yMove)

			if pygame.sprite.spritecollide(self, block_group, False):
				self.rect.move_ip(-self.xMove, -self.yMove)
				self.yMove = 0
				self.xMove = 0
				self.direction = 0
				self.nextdir = 0
		else:
			self.direction = 0


class Ghost(basicSprite.Sprite):
	"""This is our ghost that will move around the screen"""

	def __init__(self, centerPoint, image):

		basicSprite.Sprite.__init__(self, centerPoint, image)
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
