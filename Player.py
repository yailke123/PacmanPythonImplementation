import snakeSprite
from helpers import *


class Player:
	"""This is our snake that will move around the screen"""

	def __init__(self, snake):
		self.snake = snake
		self.x = 0
		self.y = 0
		self.direction = [1, 0, 0, 0]
		self.is_dead = False
		self.did_eat = False

	def move(self):
		self.snake.MoveKeyDown(K_RIGHT)
