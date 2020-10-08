#!/usr/bin/python
# -*- coding: utf-8 -*-

# Graphical Modules
import pygame
import win32api
import win32con
import win32gui

# Other
from random import randint

WIN_WIDTH = 1280 # Window Width
WIN_HEIGHT = 720 # Window Height

INIT_VEL = 0.1 # Initial Velocity - How fast the text moves

# Name of a popular font OR relative filepath to a .ttf file
FONT_NAME = 'impact'

FONT_SIZE = 30 # How big the text is
FONT_Y_MARGIN = FONT_SIZE // 10 # Text y hitbox margin
FONT_COLOR = (194, 24, 7) # Color of the text

BLACK = (2, 2, 2)  # Transparency color

class Text:
	def __init__(self, img, w, h, x, y, x_vel, y_vel):
		self.img = img # Pygame Image Object to draw
		self.w = w # Image width
		self.h = h # Image height
		self.x = x # X position
		self.y = y # Y Position
		self.x_vel = x_vel # X Velocity
		self.y_vel = y_vel # Y Velocity

class Image:
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
	font = pygame.font.SysFont(FONT_NAME, FONT_SIZE) # Initialize font object
	
	texts = []
	with open(input('Enter the filepath/name of a text file: '), 'r') as file: # Get text file from user
		for line in file:
			# Split the line into a list of words
			words = line.split()
			for word in words:
				# Create pygame Image object
				img = font.render(word, True, FONT_COLOR)
				w = img.get_width()
				h = img.get_height()
				
				# Randomize starting position
				x = randint(10, WIN_WIDTH - w - 10)
				y = randint(10, WIN_HEIGHT - h - 10)
				
				# Randomize starting direction
				dir = randint(1, 4)
				if dir == 1:
					x_vel = INIT_VEL
					y_vel = INIT_VEL
				elif dir == 2:
					x_vel = -INIT_VEL
					y_vel = INIT_VEL
				elif dir == 3:
					x_vel = -INIT_VEL
					y_vel = -INIT_VEL
				else:
					x_vel = INIT_VEL
					y_vel = -INIT_VEL
				
				# Add text to list
				texts.append(Text(img, w, h, x, y, x_vel, y_vel))
	
	return texts

# Gets the image to bounce around from user
def getImage():
	img = pygame.image.load(input('Enter the filepath/name of an image: '))
	
	w = img.get_width()
	h = img.get_height()
	
	if w > WIN_WIDTH or h > WIN_HEIGHT:
		print(f'Image ({w}x{h}) is too large for window ({WIN_WIDTH}x{WIN_HEIGHT})')
		exit()
	
	# Randomize starting position
	x = randint(0, WIN_WIDTH - w)
	y = randint(0, WIN_HEIGHT - h)
	
	# Randomize starting direction
	dir = randint(1, 4)
	if dir == 1:
		x_vel = INIT_VEL
		y_vel = INIT_VEL
	elif dir == 2:
		x_vel = -INIT_VEL
		y_vel = INIT_VEL
	elif dir == 3:
		x_vel = -INIT_VEL
		y_vel = -INIT_VEL
	else:
		x_vel = INIT_VEL
		y_vel = -INIT_VEL
	
	return Image(img, w, h, x, y, x_vel, y_vel)

def textBouncer():
	global WIN_WIDTH, WIN_HEIGHT
	
	texts = getText()
	
	clock = pygame.time.Clock()
	dt = clock.tick(60)
	
	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
	pygame.display.set_caption('Text Bouncer')
	pygame.display.set_icon(pygame.image.load('res/icon.png'))
	
	# Set window transparency color
	hwnd = pygame.display.get_wm_info()['window']
	win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
	win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*BLACK), 0, win32con.LWA_COLORKEY)
	
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.VIDEORESIZE:
				WIN_WIDTH = event.w
				WIN_HEIGHT = event.h
				screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
				texts[0].w = WIN_WIDTH/2
				texts[0].h = WIN_HEIGHT/2
		
		screen.fill(BLACK) # Set transparent background
		
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
			
			text.x += text.x_vel * dt
			text.y += text.y_vel * dt
			
			screen.blit(text.img, (int(text.x), int(text.y)))
		
		pygame.display.update()
		
		dt = clock.tick(60)
	
	pygame.display.quit()

def imageBouncer():
	global WIN_WIDTH, WIN_HEIGHT
	
	img = getImage()
	
	clock = pygame.time.Clock()
	dt = clock.tick(60)
	
	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
	pygame.display.set_caption('Image Bouncer')
	pygame.display.set_icon(pygame.image.load('res/icon.png'))
	
	# Set window transparency color
	hwnd = pygame.display.get_wm_info()['window']
	win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
	win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*BLACK), 0, win32con.LWA_COLORKEY)
	
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.VIDEORESIZE:
				WIN_WIDTH = event.w
				WIN_HEIGHT = event.h
				screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
		
		screen.fill(BLACK) # Set transparent background
		
		if img.x + img.w >= WIN_WIDTH:
			img.x_vel = -INIT_VEL
			img.x = WIN_WIDTH - img.w
		elif img.x <= 0:
			img.x_vel = INIT_VEL
			img.x = 0
		
		if img.y + img.h >= WIN_HEIGHT:
			img.y_vel = -INIT_VEL
			img.y = WIN_HEIGHT - img.h
		elif img.y <= 0:
			img.y_vel = INIT_VEL
			img.y = 0
		
		if dt < 100:
			img.x += img.x_vel * dt
			img.y += img.y_vel * dt
		
		screen.blit(img.img, (int(img.x), int(img.y)))
		
		pygame.display.update()
		
		dt = clock.tick(60)
	
	pygame.display.quit()

def main():
	pygame.init() # Initialize pygame
	
	while True:
		choice = input('Enter 1, 2, or 3:\n1. Text Bouncer\n2. Image Bouncer\n3. Exit\n')
		if choice == '1' or choice.lower() == 'text bouncer':
			textBouncer()
		elif choice == '2' or choice.lower() == 'image bouncer':
			imageBouncer()
		elif choice == '3' or choice.lower() == 'exit':
			break

if __name__ == '__main__':
	main()
