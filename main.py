from pygame import *
import pygame
import sys
import Data.text as text
pygame.init()
global display_dimensions, scale 
scale = 3
display_dimensions = [384,216]
display = pygame.Surface(display_dimensions)

win = pygame.display.set_mode((display_dimensions[0] * scale, display_dimensions[1] * scale),0,32)
global up_key, down_key, right_key, left_key, hand_key, select_key, pause_key, c_scheme
up_key = K_UP
down_key = K_DOWN
right_key = K_RIGHT
left_key = K_LEFT
hand_key = K_z
select_key = K_x
pause_key = K_ESCAPE
enter_key = K_RETURN

global e_colorkey
e_colorkey = (255,255,255)

global font_dat
font_dat = {'A': [3], 'B': [3], 'C': [3], 'D': [3], 'E': [3], 'F': [3], 'G': [3], 'H': [3], 'I': [3], 'J': [3], 'K': [3], 'L': [3], 'M': [5], 'N': [3], 'O': [3], 'P': [3], 'Q': [3], 'R': [3], 'S': [3], 'T': [3], 'U': [3], 'V': [3], 'W': [5], 'X': [3], 'Y': [3], 'Z': [3],
			'a': [3], 'b': [3], 'c': [3], 'd': [3], 'e': [3], 'f': [3], 'g': [3], 'h': [3], 'i': [1], 'j': [2], 'k': [3], 'l': [3], 'm': [5], 'n': [3], 'o': [3], 'p': [3], 'q': [3], 'r': [2], 's': [3], 't': [3], 'u': [3], 'v': [3], 'w': [5], 'x': [3], 'y': [3], 'z': [3],
			'.': [1], '-': [3], ',': [2], ':': [1], '+': [3], '\'': [1], '!': [1], '?': [3],
			'0': [3], '1': [3], '2': [3], '3': [3], '4': [3], '5': [3], '6': [3], '7': [3], '8': [3], '9': [3],
			'(': [2], ')': [2], '/': [3], '_': [5], '=': [3], '\\': [3], '[': [2], ']': [2], '*': [3], '"': [3], '<': [3], '>': [3], ';': [1]}


def get_text_width(text, spacing):
	global font_dat
	width = 0
	for char in text:
		if char in font_dat:
			width += font_dat[char][0] + spacing
		elif char == ' ':
			width += font_dat['A'][0] + spacing
	return width

def swap_color(img,old_c,new_c):
	global e_colorkey
	img.set_colorkey(old_c)
	surf = img.copy()
	surf.fill(new_c)
	surf.blit(img,(0,0))
	surf.set_colorkey(e_colorkey)
	return surf

global font
font = text.generate_font('Data/small_font.png',font_dat, 5, 8, (248, 248, 248))

pygame.display.set_caption("Game")
background = pygame.image.load('Data/background.jpg')
rightSprite = pygame.image.load('Data/rightSprite.png')
leftSprite = pygame.image.load('Data/image-2.png')


def run_menu():
	global up_key, down_key, right_key, left_key, hand_key, select_key, enter_key
	menu_bar = pygame.image.load('Data/menu_bar.png')
	selection = 0
	menu_layout = ['Play', 'Options', 'Quit']
	run = True
	while run:
		display.fill((31, 40, 54))
		n = 0
		for option in menu_layout:
			bar_img = menu_bar.copy()
			if (n == selection):
				bar_img = swap_color(bar_img, (50, 60, 95), (94, 115, 166))
			display.blit(bar_img, (26+n*140, 182))
			text.show_text(option, 53+n*140-int(get_text_width(option, 1)/2), 186, 1, 999, font, display)
			n += 1
		pressed_select = False
		pressed_right = False
		pressed_left = False
		pressed_up = False
		pressed_down = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key in [select_key, enter_key]:
					pressed_select = True
					selected_once = True
				if event.key == right_key:
					pressed_right = True
				if event.key == left_key:
					pressed_left = True
				if event.key == up_key:
					pressed_up = True
				if event.key == down_key:
					pressed_down = True
		if pressed_select:
			menu_choice = menu_layout[selection]
			if menu_choice == 'Quit':
				pygame.quit()
				sys.exit()
			if menu_choice == 'Play':
				run = False
			if menu_choice == 'Options':
				print('Work in progress!')
		if pressed_right:
			selection += 1
			if selection >= len(menu_layout):
				selection = 0
		if pressed_left:
			selection -= 1
			if selection <= -1:
				selection = 2
		win.blit(pygame.transform.scale(display,(display_dimensions[0] * scale, display_dimensions[1] * scale)),(0,0))
		pygame.display.update()

x = 200
y = 200
width = 64
height = 64

vel = 5
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0

def GameWindow():
	global walkCount
	display.blit(background,(0,0))
	#if walkCount + 1 >= 27
	if left:
		display.blit(leftSprite,(x,y))
		print("here")
	elif right:
		display.blit(rightSprite,(x,y))
	else:
		display.blit(rightSprite,(x,y))
	win.blit(pygame.transform.scale(display,(display_dimensions[0] * scale, display_dimensions[1] * scale)),(0,0))
	pygame.display.update()

run_menu()
run = True
while run:
	pygame.time.delay(30)
	for event in pygame.event.get():
		 if event.type == pygame.QUIT:
			 run = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT] and x > 0:
		x -= vel
		left = True
		right = False
	elif keys[pygame.K_RIGHT] and x < 500 - width - vel:
		x += vel
		left = False
		right = True
	else:
		right = False
		left = False
		walkCount = 0
	if not(isJump):
		# if keys[pygame.K_UP] and y > vel:
		#     y -= vel
		#if keys[pygame.K_DOWN] and y < 500 - height - vel:
		#    y += vel
		if keys[pygame.K_SPACE]:

			isJump = True
			right = False
			left = False
			walkCount = 0
	else:
		if jumpCount >= -10:
			neg = 1
			if jumpCount < 0:
				neg = -1
			y -= (jumpCount ** 2) *.5 * neg
			jumpCount -= 1
		else:
			isJump = False
			jumpCount = 10
	GameWindow()
pygame.quit()