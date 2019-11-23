import snakeSprite
from helpers import *


class Player:
	"""This is our snake that will move around the screen"""

	def __init__(self, snake):
		self.snake = snake

	def move(self):
		self.snake.MoveKeyDown(K_RIGHT)