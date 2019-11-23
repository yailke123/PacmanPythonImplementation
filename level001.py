#! /usr/bin/env python
# -*- coding: utf-8 -*-

from helpers import load_image

class Level:
    """The Base Class for Levels"""
    def getLayout(self):
        """Get the Layout of the level"""
        """Returns a [][] list"""
        pass
    def getImages(self):
        """Get a list of all the images used by the level"""
        """Returns a list of all the images used.  The indices 
        in the layout refer to sprites in the list returned by
        this function"""
        pass

class level(Level):
    """Level 1 of the PyMan Game"""
    
    def __init__(self):
        self.PELLET = 0
        self.BLOCK = 1
        self.SNAKE = 2
	self.GWALL =3
	self.GHOST =4
	self.GHOST2 =5
	self.GHOST3 =6
	self.GHOST4 =7
	
    def getLayout(self):
        return [[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9 ,9, 9, 9, 9, 9, 9, 9, 9, 9, 9],\
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9 ,9, 9, 9, 9, 9, 9, 9, 9, 9, 9],\
                [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, 1, 1, 1, 1, 1, 1, 9],\
                [9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ,0, 0, 0, 0, 0, 0, 0, 0, 1, 9],\
                [9, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1 ,0, 1, 1, 1, 0, 1, 1, 0, 1, 9],\
                [9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1, 9],\
                [9, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1 ,1, 1, 0, 1, 0, 1, 1, 0, 1, 9],\
                [9, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1 ,0, 0, 0, 1, 0, 0, 0, 0, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 0, 0, 7, 0, 0, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 1, 1, 3, 1, 1, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 0, 0, 0, 0, 0, 0, 1, 4, 5, 6, 1, 0, 0, 0, 0, 0, 0, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 9],\
                [9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9],\
                [9, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 9],\
                [9, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9],\
                [9, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 9],\
                [9, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 9],\
                [9, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 9],\
                [9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9],\
                [9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9]]
                
        
    def getSprites(self):
        block, rect = load_image('block.png')
        pellet, rect = load_image('pellet.png',-1)
        snake, rect = load_image('snake.png',-1)
	gwall, rect = load_image('gwall.png')
	ghost, rect = load_image('ghost.png',-1)
	ghost2, rect = load_image('ghost2.png',-1)
	ghost3, rect = load_image('ghost3.png',-1)
	ghost4, rect = load_image('ghost4.png',-1)
        return [pellet,block,snake,gwall,ghost,ghost2,ghost3,ghost4]
        