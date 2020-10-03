#!/usr/bin/python
# -*- coding: utf-8 -*-

# Graphical Modules
import pygame
import win32api
import win32con
import win32gui

# Other
from random import randint

WIN_WIDTH = 500 # Window Width
WIN_HEIGHT = 500 # Window Height

INIT_VEL = 0.5 # Initial Velocity - How fast the text moves

FONT_SIZE = 50 # How big the text is
FONT_Y_MARGIN = FONT_SIZE // 10 # Text y hitbox margin
FONT_COLOR = (194, 24, 7) # Color of the text

FUCHSIA = (255, 0, 128)  # Transparency color

class Text:
	def __init__(self, img, w, h, x, y, x_vel, y_vel):
		self.img = img # Pygame Image Object to draw
		self.w = w # Image width
		self.h = h # Image height
		self.x = x # X position
		self.y = y # Y Position
		self.x_vel = x_vel # X Velocity
		self.y_vel = y_vel # Y Velocity

# Gets the text to bounce around from user
def getText():
	font = pygame.font.SysFont(None, FONT_SIZE) # Initialize font object
	
	# Dummy blank Text that stays in the middle of the screen
	dummy = Text(font.render('', True, FONT_COLOR), 0, 0, WIN_WIDTH/2, WIN_HEIGHT/2, 0, 0)
	
	# The first item in texts always jitters, dummy will take the hit here
	texts = [dummy]
	with open(input('Enter the name of a text file: '), 'r') as file: # Get text file from user
		for line in file:
			# Split the line into a list of words
			words = line.split()
			for word in words:
				# Create pygame Image object
				img = font.render(word, True, FONT_COLOR)
				w = img.get_width()
				h = img.get_height()
				
				# Randomize starting position
				x = randint(0, WIN_WIDTH - w)
				y = randint(0, WIN_HEIGHT - h)
				# Add text to list
				texts.append(Text(img, w, h, x, y, INIT_VEL, INIT_VEL))
	
	return texts

def main():
	global WIN_WIDTH, WIN_HEIGHT
	
	pygame.init() # Initialize pygame
	
	texts = getText()
	
	clock = pygame.time.Clock()
	
	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
	pygame.display.set_caption('Text Bouncer')
	pygame.display.set_icon(pygame.image.load('icon.png'))
	
	# Set window transparency color
	hwnd = pygame.display.get_wm_info()['window']
	win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
	win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*FUCHSIA), 0, win32con.LWA_COLORKEY)
	
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.VIDEORESIZE:
				WIN_WIDTH = event.w
				WIN_HEIGHT = event.h
				screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
				texts[0].w = WIN_WIDTH/2
				texts[0].h = WIN_HEIGHT/2
			if event.type == pygame.QUIT:
				done = True
				exit()
		
		screen.fill(FUCHSIA) # Set transparent background
		
		for text in texts: # Draw Texts + check window edge collision
			if text.x + text.w >= WIN_WIDTH:
				text.x_vel = -INIT_VEL
				text.x = WIN_WIDTH - text.w
			elif text.x <= 0:
				text.x_vel = INIT_VEL
				text.x = 0
			
			if text.y + text.h - FONT_Y_MARGIN >= WIN_HEIGHT:
				text.y_vel = -INIT_VEL
				text.y = WIN_HEIGHT - text.h + FONT_Y_MARGIN
			elif text.y + FONT_Y_MARGIN <= 0:
				text.y_vel = INIT_VEL
				text.y = -FONT_Y_MARGIN
			
			dt = clock.tick(1000)
			
			text.x += text.x_vel * dt
			text.y += text.y_vel * dt
			
			screen.blit(text.img, (int(text.x), int(text.y)))
		
		pygame.display.update()

if __name__ == '__main__':
	main()
