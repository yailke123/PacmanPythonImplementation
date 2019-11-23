#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import basicSprite
from helpers import *
from random import randint


class Snake(basicSprite.Sprite):
    """This is our snake that will move around the screen"""
    def __init__(self, centerPoint, image):
        
        basicSprite.Sprite.__init__(self, centerPoint, image)
        """Initialize the number of pellets eaten"""
        self.pellets = 0
        """Set the number of Pixels to move each time"""
        self.dist=3
        """Initialize how much we are moving"""
        self.xMove = 0
        self.yMove = 0

	self.score=0

	self.direction=0
	self.nextdir=0
	self.xdir=[0,-self.dist,self.dist,0,0]
	self.ydir=[0,0,0,-self.dist,self.dist]


    def MoveKeyDown(self, key):
        """This function sets the xMove or yMove variables that will
        then move the snake when update() function is called.  The
        xMove and yMove values will be returned to normal when this 
        keys MoveKeyUp function is called."""
        
	self.direction=self.nextdir

        if (key == K_RIGHT):
		self.nextdir=2
        elif (key == K_LEFT):
		self.nextdir=1
        elif (key == K_UP):
		self.nextdir=3
        elif (key == K_DOWN):
		self.nextdir=4

            
    def update(self,block_group):
        """Called when the Snake sprit should update itself"""
	self.xMove=self.xdir[self.nextdir]
	self.yMove=self.ydir[self.nextdir]

        self.rect.move_ip(self.xMove,self.yMove)

        """IF we hit a block, don't move - reverse the movement"""
        if pygame.sprite.spritecollide(self, block_group, False):
		self.rect.move_ip(-self.xMove,-self.yMove)
		"""IF we can't move in the new direction... continue in old direction"""
		self.xMove=self.xdir[self.direction]
		self.yMove=self.ydir[self.direction]
		self.rect.move_ip(self.xMove,self.yMove)
		
		if pygame.sprite.spritecollide(self, block_group, False):
			self.rect.move_ip(-self.xMove,-self.yMove)
			self.yMove=0
			self.xMove=0
			self.direction=0
			self.nextdir=0
	else:
		self.direction=0



class Ghost(basicSprite.Sprite):
    """This is our ghost that will move around the screen"""
    def __init__(self, centerPoint, image):
        
        basicSprite.Sprite.__init__(self, centerPoint, image)
        """Initialize the number of pellets eaten"""
        self.pellets = 0
        """Set the number of Pixels to move each time"""
        self.dist=2

        """Initialize how much we are moving"""
        self.xMove = 0
        self.yMove = 0

	self.direction=1
	self.nextdir=3
	self.xdir=[0,-self.dist,self.dist,0,0]
	self.ydir=[0,0,0,-self.dist,self.dist]
            
    def update(self,block_group):
        """Called when the Ghost sprit should update itself"""
	#print self.nextdir,self.direction

	self.xMove=self.xdir[self.nextdir]
	self.yMove=self.ydir[self.nextdir]
	
        self.rect.move_ip(self.xMove,self.yMove)

        if pygame.sprite.spritecollide(self, block_group, False):
		self.rect.move_ip(-self.xMove,-self.yMove)

		self.xMove=self.xdir[self.direction]
		self.yMove=self.ydir[self.direction]
		self.rect.move_ip(self.xMove,self.yMove)
		
		if pygame.sprite.spritecollide(self, block_group, False):
			self.rect.move_ip(-self.xMove,-self.yMove)
			if self.nextdir<3:
				self.nextdir=randint(3,4)
			else:
				self.nextdir=randint(1,2)
	else:
		self.direction=self.nextdir
		if self.nextdir<3:
			self.nextdir=randint(3,4)
		else:
			self.nextdir=randint(1,2)



