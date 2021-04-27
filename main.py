from pygame import *
import pygame
import sys
import Data.text as text
def load_video_settings():
	global scale
	f= open('Data/video_settings.txt', 'r')
	dat = f.read()
	scale = int(dat[0])
	f.close()
	return dat[1]
def save_video_settings():
	global fullscreened, scale
	f = open('Data/video_settings.txt', 'w')
	f.write(str(scale) + fullscreened)
	f.close()
pygame.init()
global display_dimensions, scale, fullscreened
display_dimensions = [384,216]
fullscreened = load_video_settings()
global win
if fullscreened == 'n':
	win = pygame.display.set_mode((display_dimensions[0] * scale, display_dimensions[1] * scale),0,32)
else:
	win = pygame.display.set_mode((display_dimensions[0] * scale, display_dimensions[1] * scale),pygame.FULLSCREEN)
	
display = pygame.Surface(display_dimensions)


global up_key, down_key, right_key, left_key, power_key, select_key, pause_key, c_scheme
up_key = K_UP
down_key = K_DOWN
right_key = K_RIGHT
left_key = K_LEFT
power_key = K_z
select_key = K_RETURN
pause_key = K_ESCAPE
enter_key = K_RETURN

def load_controls():
	global up_key, down_key, right_key, left_key, power_key, select_key, pause_key, c_scheme
	f = open('Data/control_settings.txt','r')
	dat = f.read()
	f.close()
	control_dat = dat.split('\n')[0]
	if control_dat == 'default':
		c_scheme = 'default'
	else:
		c_scheme = 'custom'
		n = 0
		for val in control_dat.split(';'):
			if n == 0:
				up_key = int(val)
			if n == 1:
				down_key = int(val)
			if n == 3:
				left_key = int(val)
			if n == 4:
				power_key = int(val)
			if n == 5:
				select_key = int(val)
			n += 1 
def save_controls():
	global up_key, down_key, right_key, left_key, power_key, select_key, c_scheme
	f = open('Data/control_settings.txt','r')
	dat = f.read()
	f.close()
	dat = dat.split('\n')
	f = open('Data/control_settings.txt','w')
	out_str = str(up_key) + ';' + str(down_key) + ';' + str(right_key) + ';' + str(left_key) + ';' + str(power_key) + ';' + str(select_key) + '\n' + dat[1]
	f.write(out_str)
	f.close()
load_controls()
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
font_3 = text.generate_font('Data/small_font.png',font_dat,5,8,(16,30,41))

pygame.display.set_caption("Game")
background = pygame.image.load('Data/background.jpg')
rightSprite = pygame.image.load('Data/walk.gif')
leftSprite = pygame.image.load('Data/walk.gif')


def run_menu():
	global up_key, down_key, right_key, left_key, power_key, select_key, enter_key
	menu_bar = pygame.image.load('Data/menu_bar.png')
	title_img = pygame.image.load('Data/SlimeByte.png')
	selection = 0
	menu_layout = ['Play', 'Options', 'Quit']
	run = True
	while run:
		display.fill((31, 40, 54))
		display.blit(title_img,(50,0))
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
				make_menu('options')
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

def make_menu(menu_id):
	global up_key, down_key, right_key, left_key, power_key, select_key, enter_key, pause_key, scale, win
	global display_dimensions
	options_bar = pygame.image.load('Data/options_bar.png')
	wide_bar = pygame.image.load('Data/wide_bar.png')
	wide = False
	if menu_id == 'pause' :
		menu_options = ['Resume','Exit to Main Menu']
		menu_title = 'Paused'
	if menu_id == 'options':
		menu_options = ['Video','Keybinds','Back']
		menu_title = 'Options'
	if menu_id == 'video':
		menu_options = ['384x216','768x432','1152x648','1536x684','1920x1080', 'Fullscreen','Back']
		menu_title = 'Video Settings'
	if menu_id == 'keyboard':
		menu_options = ['Left: ','Right: ','Up/Jump: ','Down: ','Use Special: ','Select: ','Pause: ','Back']
		wide = True
		menu_title = 'Keyboard Settings'
		key_order = [left_key,right_key,up_key,down_key,power_key,select_key,pause_key]
	setting_key = 0
	current_selection = 0
	running = True 
	return_val = None

	while running:
		display.blit(background,(0,0))
		title_surf = pygame.Surface((display_dimensions[0],14))
		title_surf.fill((50,60,95))
		display.blit(title_surf,(0,24))
		text.show_text(menu_title,int((display_dimensions[0]-get_text_width(menu_title,1))/2),28,1,999,font,display)
		n = 0
		for option in menu_options:
			bar_img = options_bar.copy()
			if wide:
				bar_img = wide_bar.copy()
			if n == current_selection:
				bar_img = swap_color(bar_img,(50,60,95),(94,115,166))
			display.blit(bar_img,(26,50+n*20))
			ending = ''
			if menu_id == 'keyboard':
				if n <=6:
					ending =pygame.key.name(key_order[n])
				if (setting_key == 1) and (current_selection == n):
					ending = 'press a key'
			text.show_text(option+ending,31,54+n*20,1,999,font,display)
			if menu_id == 'video':
				if option == 'Fullscreen':
					if n == current_selection:
						text.show_text('Scaling is affected by windowed resolution.',131,55+n*20,1,999,font_3,display)
						text.show_text('Scaling is affected by windowed resolution.',130,54+n*20,1,999,font,display)
				if option == '1920x1080':
					if n == current_selection:
						text.show_text('This may lag.',131,55+n*20,1,999,font_3,display)
						text.show_text('This may lag.',130,54+n*20,1,999,font,display)
			n += 1
		pressed_select = False
		pressed_up = False
		pressed_down = False
		if setting_key == 0:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:
					if event.key in [select_key,enter_key]:
						pressed_select = True
					if event.key == right_key:
						pressed_right = True
					if event.key == left_key:
						pressed_left = True
					if event.key == up_key:
						pressed_up = True
					if event.key == down_key:
						pressed_down = True
		if setting_key == 0:
			if pressed_select:
				chosen_option = menu_options[current_selection]
				if menu_id == 'pause':
					if chosen_option == 'Resume':
						running = False
						return_val = False
					if chosen_option == 'Exit to Main Menu':
						running = False
						return_val = False
						run_menu()
				if menu_id == 'options':
					if chosen_option == 'Video':
						make_menu('video')
					if chosen_option == 'Keybinds':
						make_menu('keyboard')
					if chosen_option == 'Back':
						running = False
				if menu_id == 'video':
					if chosen_option == 'Back':
						running = False
					elif chosen_option == 'Fullscreen':
						fullscreened = 'y'
						win = pygame.display.set_mode((display_dimensions[0] * scale, display_dimensions[1] * scale),pygame.FULLSCREEN)
					else:
						fullscreened = 'n'
						scale = current_selection + 1
						win = pygame.display.set_mode((display_dimensions[0] * scale, display_dimensions[1] * scale),0,32)
					save_video_settings()
				if menu_id == 'keyboard':
					if chosen_option == 'Back':
						running = False
					else:
						setting_key = 1
			if pressed_down:
				current_selection += 1
				if current_selection >= len(menu_options):
					current_selection = 0
			if pressed_up:
				current_selection -= 1
				if current_selection < 0:
					current_selection = len(menu_options)-1
		else:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					setting_key = 0
					if event.key not in key_order:
						if current_selection == 0:
							left_key = event.key
						if current_selection == 1:
							right_key = event.key
						if current_selection == 2:
							up_key = event.key
						if current_selection == 3:
							down_key = event.key
						if current_selection == 4:
							power_key = event.key
						if current_selection == 5:
							select_key = event.key
						if current_selection == 6:
							pause_key = event.key
					key_order = [left_key,right_key,up_key,down_key,power_key,select_key,pause_key]
					save_controls()
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
		win.blit(pygame.transform.scale(display,(display_dimensions[0] * scale, display_dimensions[1] * scale)),(0,0))
		pygame.display.update()
					





x = 100
y = 100
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
		if event.type == KEYDOWN:
			if event.key == pause_key:
				make_menu('pause')
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