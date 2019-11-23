#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
import level001
import basicSprite
from pygame.locals import *
from pygame import mixer
from helpers import *
from snakeSprite import Snake,Ghost
from menu import *
from image import *

# TODO
# > add power pills
# > add quit option
# > improve sound substructure
# > add better object code and polymorphism
# > add cherries etc / powerups
# > choose control of ghost / pacman
# > option submenu


clock = pygame.time.Clock()

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

BLOCK_SIZE = 24


def mainmenu(screen):

	menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
		[('Start Game', 1, None),
		('Options',    2, None),
		('Exit',       3, None)])

	menu_options = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                [('Back',  0, None),
                 ('opt 1',      200, None),
		 ('opt 2',      200, None)])


	# Center the menu on the draw_surface (the entire screen here)
	menu.set_center(True, True)
	menu_options.set_center(True, True)
	# Center the menu on the draw_surface (the entire screen here)
	menu.set_alignment('center', 'center')

	# Create the state variables (make them different so that the user event is
	# triggered at the start of the "while 1" loop so that the initial display
	# does not wait for user input)
	state = 0
	prev_state = 1

	# rect_list is the list of pygame.Rect's that will tell pygame where to
	# update the screen (there is no point in updating the entire screen if only
	# a small portion of it changed!)
	rect_list = []

	# Ignore mouse motion (greatly reduces resources when not needed)
	pygame.event.set_blocked(pygame.MOUSEMOTION)

	# The main while loop
	while 1:
		# Check if the state has changed, if it has, then post a user event to
		# the queue to force the menu to be shown at least once
		
		print prev_state,state
		
		if prev_state != state:
			print state
			bkg = load_image('bkg.jpg','data/images')
			screen.blit(bkg, (0, 0))
			pygame.display.flip()
			
			pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
			prev_state = state

		# Get the next event
		e = pygame.event.wait()

		# Update the menu, based on which "state" we are in - When using the menu
		# in a more complex program, definitely make the states global variables
		# so that you can refer to them by a name
		if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
			if state == 0:
				rect_list, state = menu.update(e, state)
			elif state == 1:
				break
				state = 0
			elif state == 2:
				rect_list, state = menu_options.update(e, state)
				print 'Options!',state
			else:
				print 'Exit!'
				pygame.quit()
				sys.exit()

		# Quit if the user presses the exit button
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Update the screen
		pygame.display.update(rect_list) 


class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=480):
        """Initialize"""
        pygame.init()
	
        """Set the window Size"""
        self.width = width
        self.height = height
	
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))
	pygame.display.set_caption("Mac Pan - Matthew Rollings")
	
	
	# Setup the sounds
	pygame.mixer.init()
	self.sounds={'die':mixer.Sound("die.ogg"),'intro':mixer.Sound("intro.ogg")}

	self.sounds['intro'].play()
	
	# Setup the variables
	self.collisiontol=5;
	self.collisions=0;

    def MainLoop(self):
        """This is the Main Loop of the Game"""
	while 1:
		mainmenu(self.screen)
		"""Load All of our Sprites"""
		self.LoadSprites();
		
		"""Create the background"""
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0,0,0))
		"""Draw the blocks onto the background, since they only need to be 
		drawn once"""
		self.block_sprites.draw(self.background)
		self.gwall_sprites.draw(self.background)

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()
				elif event.type == KEYDOWN: #or event.type == KEYUP
					if ((event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP) or (event.key == K_DOWN)):
						self.snake.MoveKeyDown(event.key)

			"""Update the sprites"""        
			self.snake_sprites.update(self.block_sprites)
			self.ghost_sprites.update(self.block_sprites)     
			self.ghost2_sprites.update(self.block_sprites) 
			self.ghost3_sprites.update(self.block_sprites) 
			self.ghost4_sprites.update(self.block_sprites) 
			
			if pygame.sprite.collide_rect(self.ghost,self.snake) or pygame.sprite.collide_rect(self.ghost2,self.snake) or pygame.sprite.collide_rect(self.ghost3,self.snake) or pygame.sprite.collide_rect(self.ghost4,self.snake):
				self.collisions+=1
				print "Col+1",self.collisions
				if self.collisions==self.collisiontol:
					print "gameover"
					break
			else:
				self.collisions=0

			"""Check for a snake collision/pellet collision"""
			lstCols = pygame.sprite.spritecollide(self.snake, self.pellet_sprites, True)
			"""Update the amount of pellets eaten"""
			self.snake.pellets = self.snake.pellets + len(lstCols)
			self.score=self.snake.pellets*10
				
			"""Do the Drawing"""               
			self.screen.blit(self.background, (0, 0))
			if pygame.font:
				font = pygame.font.Font(None, 36)
				text = font.render("Score %s" % self.score, 1, (255, 255, 255))
				textpos = text.get_rect(x=0)
				self.screen.blit(text, textpos)
			
			self.pellet_sprites.draw(self.screen)
			self.snake_sprites.draw(self.screen)
			self.ghost_sprites.draw(self.screen)
			self.ghost2_sprites.draw(self.screen)
			self.ghost3_sprites.draw(self.screen)
			self.ghost4_sprites.draw(self.screen)
			pygame.display.flip()
			clock.tick(40)
			#print clock.get_fps()
		self.sounds['die'].play()
        
    def LoadSprites(self):
        """Load all of the sprites that we need"""
        """calculate the center point offset"""
        x_offset = (BLOCK_SIZE/2)
        y_offset = (BLOCK_SIZE/2)
        """Load the level"""        
        level1 = level001.level()
        layout = level1.getLayout()
        img_list = level1.getSprites()

        self.pellet_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.gwall_sprites = pygame.sprite.Group()

        for y in xrange(len(layout)):
            for x in xrange(len(layout[y])):
                """Get the center point for the rects"""
                centerPoint = [(x*BLOCK_SIZE)+x_offset,(y*BLOCK_SIZE+y_offset)]
                if layout[y][x]==level1.BLOCK:
                    self.block_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.BLOCK]))
                elif layout[y][x]==level1.GWALL:
                    self.gwall_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.GWALL]))
                elif layout[y][x]==level1.SNAKE:
                    self.snake = Snake(centerPoint,img_list[level1.SNAKE])
                elif layout[y][x]==level1.PELLET:
                    self.pellet_sprites.add(basicSprite.Sprite(centerPoint, img_list[level1.PELLET]))
                elif layout[y][x]==level1.GHOST:
                    self.ghost = Ghost(centerPoint,img_list[level1.GHOST])
                elif layout[y][x]==level1.GHOST2:
                    self.ghost2 = Ghost(centerPoint,img_list[level1.GHOST2]) 
                elif layout[y][x]==level1.GHOST3:
                    self.ghost3 = Ghost(centerPoint,img_list[level1.GHOST3])  
                elif layout[y][x]==level1.GHOST4:
                    self.ghost4 = Ghost(centerPoint,img_list[level1.GHOST4])  
        """Create the Snake group"""            
        self.snake_sprites = pygame.sprite.RenderPlain((self.snake))                                  
	self.ghost_sprites = pygame.sprite.RenderPlain((self.ghost))      
	self.ghost2_sprites = pygame.sprite.RenderPlain((self.ghost2))    
	self.ghost3_sprites = pygame.sprite.RenderPlain((self.ghost3))
	self.ghost4_sprites = pygame.sprite.RenderPlain((self.ghost4))
if __name__ == "__main__":
	MainWindow = PyManMain(500,575)
	MainWindow.MainLoop()
       