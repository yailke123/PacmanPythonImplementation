# -*- coding: utf-8 -*-
import pygame

from menu import cMenu

menu = cMenu(50, 50, 20, 5, 'vertical', 100, self.screen,
		[('Start Game', 1, None),
		('Options', 2, None),
		('Exit', 3, None)])

# Center the menu on the draw_surface (the entire screen here)
menu.set_center(True, True)

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
	if prev_state != state:
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
			print 'Options!'
			state = 0
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