from pygame import *
import pygame
import sys
import Data.text as text
import time

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
mainClock = pygame.time.Clock()
pygame.init()
global display_dimensions, scale, fullscreened
display_dimensions = [384,216]
fullscreened = load_video_settings()
global win
level1Music = pygame.mixer.Sound('Data/level1.mp3')
level2Music = pygame.mixer.Sound('Data/level2.mp3')
MenuMusic = pygame.mixer.Sound('Data/menu.mp3')
jumpSound = pygame.mixer.Sound('Data/slime animations/jump.wav')
powerup = pygame.mixer.Sound('Data/slime animations/powerup.wav')
dieSound = pygame.mixer.Sound('Data/slime animations/die.wav')
damage = pygame.mixer.Sound('Data/slime animations/damage.wav')
explosionSound = pygame.mixer.Sound('Data/slime animations/explosion.wav')
shootNormalSound = pygame.mixer.Sound('Data/slime animations/shootNormal.wav')
win = pygame.mixer.Sound('Data/slime animations/win.wav')
menu_move = pygame.mixer.Sound('Data/slime animations/menu_move.wav')
menu_select = pygame.mixer.Sound('Data/slime animations/menu_select.wav')
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
power_key = K_SPACE
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

global framerate
framerate = 60

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
#rightSprite = pygame.image.load('Data/walk.gif')
#leftSprite = pygame.image.load('Data/walk.gif')

def opening():
	global display_dimensions
	opening_bg = pygame.image.load('Data/background.jpg')
	opening_img = pygame.image.load('Data/opening.png')
	timer = 0
	while timer < 227:
		timer += 1
		display.fill((16,30,41))
		opening_bg.set_alpha(max(0,min(int((timer-100)*5),255)))
		display.blit(opening_img,(100,60))
		if timer > 220:
			white_surf = pygame.Surface(display_dimensions)
			white_surf.fill((248,248,248))
			white_surf.set_alpha(min((timer-220)*40,255))
			display.blit(white_surf,(0,0))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		win.blit(pygame.transform.scale(display,(display_dimensions[0] * scale, display_dimensions[1] * scale)),(0,0))
		pygame.display.update()
		mainClock.tick(framerate)

def run_menu():
	global up_key, down_key, right_key, left_key, power_key, select_key, enter_key
	menu_bar = pygame.image.load('Data/menu_bar.png')
	title_img = pygame.image.load('Data/SlimeByte.png')
	pygame.mixer.music.pause()
	pygame.mixer.music.load('Data/menu.mp3')
	pygame.mixer.music.play(-1)
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
			menu_select.play()
			menu_choice = menu_layout[selection]
			if menu_choice == 'Quit':
				pygame.quit()
				sys.exit()
			if menu_choice == 'Play':
				run = False
			if menu_choice == 'Options':
				make_menu('options')
		if pressed_right:
			menu_move.play()
			selection += 1
			if selection >= len(menu_layout):
				selection = 0
		if pressed_left:
			menu_move.play()
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
		menu_options = ['Left: ','Right: ','Up/Jump: ','Down: ','Shoot: ','Select: ','Pause: ','Back']
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
				menu_select.play()
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
				menu_move.play()
				current_selection += 1
				if current_selection >= len(menu_options):
					current_selection = 0
			if pressed_up:
				menu_move.play()
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

# load some images, specifies 
def load_sprites(path, name, number, size="default", extension="png", resize_type="default", flip=(False, False)):
	sprites_list = []
	for nb in range(number):
		# load
		sprite = pygame.image.load(f"{path}/{name}{nb}.{extension}")
		# resize
		if size != "default":
			if resize_type == "default":
				sprite = pygame.transform.scale(sprite, size)
			elif resize_type == "smooth":
				sprite = pygame.transform.smoothscale(sprite, size)
		# flip
		if flip != (False, False):
			sprite = pygame.transform.flip(sprite, flip[0], flip[1])

		sprites_list.append(sprite)

	return sprites_list

class largerBullet(object):
	def __init__(self, pos, radius=30, color=(0, 200, 0)):
		x, y = pos
		self.radius = radius
		self.rect = pygame.Rect(x-radius, y-radius, radius*2, radius*2)
		self.color = color

		bonus_sprite_size = int(radius * 2)
		self.bonus_sprite = load_sprites("Data/slime animations/bonus", "largerBullet2_", 1,
										size=(bonus_sprite_size, bonus_sprite_size), resize_type="smooth")[0]


	def draw(self):
		# pygame.draw.rect(win, (222, 22, 22), self.rect) # draw the hitbox
		# pygame.draw.circle(win, self.color, self.rect.center, self.radius)
		# draw the image in the center
		win.blit(self.bonus_sprite, (self.rect.centerx - self.bonus_sprite.get_width()//2,
									self.rect.centery - self.bonus_sprite.get_height()//2))


	def activatePowerUp(self):
		global reloadBigShots
		reloadBigShots = 10
		powerUps.pop(powerUps.index(self))



class fasterBullet(object):
	def __init__(self, pos, radius=20, color=(200, 200, 200)):
		x, y = pos
		self.radius = radius
		self.rect = pygame.Rect(x-radius, y-radius, radius*2, radius*2)
		self.color = color

		bonus_sprite_size = int(radius * 2)
		self.bonus_sprite = load_sprites("Data/slime animations/bonus", "fasterBullet2_", 1,
										size=(bonus_sprite_size, bonus_sprite_size), resize_type="smooth")[0]


	def draw(self):
		# pygame.draw.rect(win, (222, 22, 22), self.rect) # draw the hitbox
		# pygame.draw.circle(win, self.color, self.rect.center, self.radius)
		# draw the image in the center
		win.blit(self.bonus_sprite, (self.rect.centerx - self.bonus_sprite.get_width()//2,
									self.rect.centery - self.bonus_sprite.get_height()//2))


	def activatePowerUp(self):
		global reloadFastShots
		reloadFastShots = 10
		powerUps.pop(powerUps.index(self))



class permaBuffSpeed(object):
	def __init__(self, pos, radius=20, color=(0,0,200)):
		x, y = pos
		self.radius = radius
		self.rect = pygame.Rect(x-radius, y-radius, radius*2, radius*2)
		self.color = color

		bonus_sprite_size = int(radius * 2)
		self.bonus_sprite = load_sprites("Data/slime animations/bonus", "permaBuffSpeed2_", 1,
										size=(bonus_sprite_size, bonus_sprite_size), resize_type="smooth")[0]


	def draw(self):
		# pygame.draw.rect(win, (222, 22, 22), self.rect) # draw the hitbox
		# pygame.draw.circle(win, self.color, self.rect.center, self.radius)
		# draw the image in the center
		win.blit(self.bonus_sprite, (self.rect.centerx - self.bonus_sprite.get_width()//2,
									self.rect.centery - self.bonus_sprite.get_height()//2))


	def activatePowerUp(self):
		powerUps.pop(powerUps.index(self))
		sprite.vel[0] = int(sprite.vel[0] * 1.5) # the player will move X time faster



class doubleBullet(object):
	def __init__(self, pos, radius=20, color=(0,0,200)):
		x, y = pos
		self.radius = radius
		self.rect = pygame.Rect(x-radius, y-radius, radius*2, radius*2)
		self.color = color

		bonus_sprite_size = int(radius * 2)
		self.bonus_sprite = load_sprites("Data/slime animations/bonus", "doubleBullet2_", 1,
										size=(bonus_sprite_size, bonus_sprite_size), resize_type="smooth")[0]


	def draw(self):
		# pygame.draw.rect(win, (222, 22, 22), self.rect) # draw the hitbox
		# pygame.draw.circle(win, self.color, self.rect.center, self.radius)
		# draw the image in the center
		win.blit(self.bonus_sprite, (self.rect.centerx - self.bonus_sprite.get_width()//2,
									self.rect.centery - self.bonus_sprite.get_height()//2))


	def activatePowerUp(self):
		global reloadDoubleShots
		reloadDoubleShots = 10
		powerUps.pop(powerUps.index(self))



class tripleBullet(object):
	def __init__(self, pos, radius=30, color=(0,0,200)):
		x, y = pos
		self.radius = radius
		self.rect = pygame.Rect(x-radius, y-radius, radius*2, radius*2)
		self.color = color

		bonus_sprite_size = int(radius * 2)
		self.bonus_sprite = load_sprites("Data/slime animations/bonus", "tripleBullet2_", 1,
										size=(bonus_sprite_size, bonus_sprite_size), resize_type="smooth")[0]


	def draw(self):
		# pygame.draw.rect(win, (222, 22, 22), self.rect) # draw the hitbox
		# pygame.draw.circle(win, self.color, self.rect.center, self.radius)
		# draw the image in the center
		win.blit(self.bonus_sprite, (self.rect.centerx - self.bonus_sprite.get_width()//2,
									self.rect.centery - self.bonus_sprite.get_height()//2))


	def activatePowerUp(self):
		global reloadTripleBullet
		reloadTripleBullet = 10
		powerUps.pop(powerUps.index(self))



class projectile(object):
	def __init__(self, x, y, radius, color, facing, vel,upOrDown = 0):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = vel * facing
		self.upOrDown = upOrDown
		self.rect = pygame.Rect(self.x-self.radius, self.y - self.radius, self.radius*2, self.radius*2) # rect for collisions


	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


	def collide(self, target_rect):
		self.rect.center = (self.x, self.y)
		# pygame.draw.rect(win, (222,22,77), self.rect) # draw the hitbox
		if self.rect.colliderect(target_rect):
			return True



class Explosion:
	def __init__(self, pos, speed=0.075, size="default"):
		self.pos = pos
		self.explosionSprites = load_sprites("Data/slime animations/sprite list/explosion", "sprite_", 7, size=size)

		self.animations_speed = speed  # the images will change every X sec
		self.current_frame = 0
		self.animations_timer = 0 # store the time for  the animations


	def make_animation(self):
		if time.time() > self.animations_timer:
			self.animations_timer = time.time() + self.animations_speed
			self.current_frame += 1 # change the frame
			if self.current_frame > len(self.explosionSprites)-1:
				return "to_remove"

		return self.explosionSprites[self.current_frame]


	def draw(self):
		sprite = self.make_animation()
		if sprite == "to_remove":
			explosionsList.pop(explosionsList.index(self))
		else:
			win.blit(sprite, (self.pos[0] - sprite.get_width()//2, self.pos[1] - sprite.get_height()//2))



class Spike(object):

	def __init__(self, pos):
		x, y = pos
		size = (50, 50) # size of the spike image
		self.lives = 2 # X bullets are needed to break the spike
		self.spikeSprites = {} # will contain all the spike sprite
		self.spikeSprites["gray"] = load_sprites("Data/slime animations/bomb/gray", "bomb_", 4, size=size)
		self.spikeSprites["red"] = load_sprites("Data/slime animations/bomb/red", "bomb_", 4, size=size)

		self.animations_speed = 0.2
		# the images will change every X sec
		self.current_frame = 0
		self.animations_timer = 0 # store the time for  the animations

		hitbox_smaller = (15, 15) # will make the spike hitbox a little bit smaller than the image
		self.rect = pygame.Rect(x - size[0]/2 + hitbox_smaller[0]/2, y - size[1] + hitbox_smaller[1],
								 size[0] - hitbox_smaller[0], size[1] - hitbox_smaller[1])


	def collide(self, target_rect): # check if the target_rect (player rect) collide with the spike
		if self.rect.colliderect(target_rect):
			explosionSound.play()
			print("target collide with spike")
			return True


	def make_animation(self): 
		if self.lives > 1:
			color = "gray"
		else:
			color = "red"

		if time.time() > self.animations_timer:
			self.animations_timer = time.time() + self.animations_speed
			self.current_frame += 1 # change the frame
			if self.current_frame > len(self.spikeSprites[color])-1:
				self.current_frame = 0

		return self.spikeSprites[color][self.current_frame]


	def draw(self):
		# pygame.draw.rect(win, (222, 22, 2), self.rect) # draw the hitbox
		sprite = self.make_animation()
		win.blit(sprite, (self.rect.centerx - sprite.get_width()//2, self.rect.bottom - sprite.get_height()))



def createSpikeLists(poslist): # create a spike at each position in the list
	listOfSpikes = []
	for pos in poslist:
		listOfSpikes.append(Spike(pos))
	return listOfSpikes


def createObstaclesLists(obstaclesPosList): # create the obstacles rect (hitbox)
	listOfObstacles = []

	for pos in obstaclesPosList:
		start_pos, end_pos = pos
		rect = pygame.Rect(start_pos[0], start_pos[1], end_pos[0]-start_pos[0], end_pos[1]-start_pos[1])
		listOfObstacles.append(rect)

	return listOfObstacles



class player(object):
	def __init__(self, x, y, width, height,vel):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.rect = pygame.Rect(x, y, width, height) # player rect

		# jump and fall settings
		self.reset_fall_speed = 3
		self.increase_fall_speed  = 1.7
		self.max_fall_speed = 20
		self.jumpHeight = 24

		self.vel = [vel, 0] # vel x, vel y

		self.isJump = False
		self.isFalling = True

		self.hitbox = (self.x, self.y, self.width, self.height)

		# sprites
		self.isLooking = "right"
		self.sprites = {"right": {}, "left": {}}
			# walk
		self.sprites["right"]["walk"] = load_sprites("Data/slime animations/sprite list/walk", "sprite_", 4, size="default")
		self.sprites["left"]["walk"] = load_sprites("Data/slime animations/sprite list/walk", "sprite_", 4, size="default", flip=(True,False))
			# jump
		self.sprites["right"]["jump"] = load_sprites("Data/slime animations/sprite list", "jump_", 1, size="default")
		self.sprites["left"]["jump"] = load_sprites("Data/slime animations/sprite list", "jump_", 1, size="default", flip=(True,False))
			# splash
		self.sprites["right"]["splash"] = load_sprites("Data/slime animations/sprite list/splash", "sprite_", 3, size="default")
		self.sprites["left"]["splash"] = load_sprites("Data/slime animations/sprite list/splash", "sprite_", 3, size="default", flip=(True,False))

		# animations
		self.state = "jump"
		self.animations_speed = {"walk": 0.2, "jump": 0.07, "splash": 0.12} # the sprite image will change every X sec
		self.current_frame = 0
		self.animations_timer = 0 # store the time for the animations




	def move(self): # make move the player

		keys = pygame.key.get_pressed()

		vel = [0, 0]
		# right and left
		if keys[pygame.K_LEFT]:
			vel[0] -= self.vel[0]
			self.isLooking = "left"
		if keys[pygame.K_RIGHT]:
			vel[0] += self.vel[0]
			self.isLooking = "right"

		self.x += vel[0]
		self.rect.x = self.x
			# make that the player can not move outside the screen
		if self.rect.right > win.get_width():
			self.rect.right = win.get_width()
			self.x = self.rect.x
		elif self.rect.left < 0:
			self.rect.left = 0
			self.x = self.rect.x


		for obstacle in obstaclesList:
			if self.rect.colliderect(obstacle): # if  the player colldie  with the obstalce
				if vel[0] < 0: # if the player is moving to the left
					self.rect.left = obstacle.right
					self.x = self.rect.x
				elif vel[0] > 0: # if the player is moving to the right
					self.rect.right = obstacle.left
					self.x = self.rect.x

		# up and down
		if not self.isJump and not self.isFalling:
			if keys[pygame.K_UP]:
				self.isJump = True
				self.vel[1] -= self.jumpHeight
				jumpSound.play()
				

		# make the gravity
		self.vel[1] += self.increase_fall_speed
		self.vel[1] = min(self.vel[1], self.max_fall_speed)

		self.y += self.vel[1]
		self.rect.y = self.y
		self.isFalling = True

		for obstacle in obstaclesList:
			if self.rect.colliderect(obstacle): # if  the player colldie  with the obstalce
				if self.vel[1] < 0: # if the player is moving up (when jumping)
					self.vel[1] = 0
					self.rect.top = obstacle.bottom
					self.y = self.rect.y
				elif self.vel[1] > 0: # if the player is moving down (falling)
					self.vel[1] = self.reset_fall_speed
					self.fall_speed = self.reset_fall_speed
					self.rect.bottom = obstacle.top
					self.y = self.rect.y
					if self.isJump:
						self.state = "splash" # will make the splash animations
						self.current_frame = 0 # will begin the splash animations with the first frame
						self.isJump = False # make that the player can jump again
					self.isFalling = False

		# draw the player hitbox
		# pygame.draw.rect(win, (255, 0, 0), self.rect)


	def make_animation(self):
		if self.isJump:
			if self.state == "walk" or self.state == "splash":
				self.current_frame = 0
			self.state = "jump"
		elif self.state != "splash":
			if self.state != "walk":
				self.current_frame = 0
			self.state = "walk"


		if time.time() > self.animations_timer:
			self.animations_timer = time.time() + self.animations_speed[self.state]
			self.current_frame += 1 # change the frame
			if self.current_frame > len(self.sprites[self.isLooking][self.state])-1:
				self.current_frame = 0
				# if not self.isJump:
				#     self.state = "walk"
				if self.state == "splash":
					self.state = "walk"

		return self.sprites[self.isLooking][self.state][self.current_frame]


	def draw(self):
		sprite = self.make_animation()
		win.blit(sprite, (self.rect.centerx-sprite.get_width()//2, self.rect.bottom-sprite.get_height()))



def GameWindow():
	# draw the obstacles hitbox
	# for obstalce in obstaclesList:
	#     pygame.draw.rect(win, (255, 222, 200), obstalce)

	if not gameOver: # only draw if the sprite player is alive
		sprite.draw()

	for powerUp in powerUps:
		powerUp.draw()

	for bullet in bullets:
		bullet.draw(win)

	for spike in spikesList:
		spike.draw()

	pygame.display.update()

opening()
run_menu()
background_level_1 = pygame.transform.scale(pygame.image.load('Data/level 1 empty.png'), (win.get_width(), win.get_height()))
background_level_2 = pygame.transform.scale(pygame.image.load('Data/level 3 empty.png'), (win.get_width(), win.get_height()))
run = True
display.blit(background, (0, 0))
previous_time = pygame.time.get_ticks()

#level 1
level_1_obstaclesPosList = [[(42, 436), (124, 452)], [(2, 588), (1151, 646)], [(146, 509), (225, 526)], [(409, 509), (489, 527)], [(773, 501), (861, 520)],
					[(1070, 501), (1149, 515)], [(978, 426), (1056, 443)], [(1072, 351), (1151, 365)], [(976, 270), (1053, 284)],
					[(1071, 194), (1149, 206)], [(815, 110), (1060, 128)], [(646, 113), (726, 131)], [(510, 304), (671, 319)],
					[(510, 114), (590, 129)], [(412, 258), (494, 273)], [(318, 302), (400, 317)], [(142, 356), (306, 371)],
					[(246, 115), (396, 129)], [(0, 88), (177, 104)]]

level_1_spikesPosList = [(443, 508), (643, 588), (205, 355), (1012, 426), (1112, 192), (551, 111), (830, 109), (919, 110), (138, 60) ,(832, 362)]


# level 2
level_2_obstaclesPosList = [[(0, 256), (88, 290)], [(76, 378), (266, 417)], [(363, 385), (474, 416)], [(563, 477), (658, 510)],
					[(728, 384), (893, 418)], [(849, 481), (961, 514)], [(1022, 558), (1148, 591)], [(1063, 391), (1151, 420)],
					[(954, 320), (1039, 348)], [(1064, 247), (1150, 278)], [(932, 181), (1011, 212)], [(762, 123), (935, 159)],
					[(532, 177), (673, 210)], [(440, 99), (529, 131)], [(317, 98), (406, 132)], [(1, 99), (87, 131)],
					[(0, 564), (106, 591)], [(170, 563), (268, 592)], [(326, 563), (414, 597)], [(1, 634), (1151, 647)],
					[(473, 545), (530, 578)]]

level_2_spikesPosList = [(31, 564), (462, 384), (365, 296), (904, 481), (1086, 557), (1106, 390), (607, 294), (482, 99), (599, 142)]

def load_level_1():
	global sprite, bullets, obstaclesList, spikesList, powerUps, reloadBigShots
	global reloadFastShots, reloadDoubleShots, reloadTripleBullet
	global explosionsList, enemies, gameOver, flagRect, current_level

	pygame.mixer.music.pause()
	pygame.mixer.music.load('Data/level1.mp3')
	pygame.mixer.music.play(-1)

	current_level = 1


	sprite = player(0, display_dimensions[1] - 64, 40, 40,5)

	enemies = []
	bullets = []

	gameOver = False

	obstaclesList = createObstaclesLists(level_1_obstaclesPosList)

	spikesList = createSpikeLists(level_1_spikesPosList)

	flagRect = pygame.Rect(22, 14, 20, 71)
	powerUps = []

	 # functional powerUp :
	powerUps.append(largerBullet((1103, 470))
					)
	#powerUps.append(fasterBullet((458,  550)))
	powerUps.append(permaBuffSpeed(((643, 564))))
	# powerUps.append(doubleBullet((794, 550)))
	powerUps.append(tripleBullet((584, 255)))


	reloadBigShots = 0
	reloadFastShots = 0
	reloadDoubleShots = 0
	reloadTripleBullet = 0

	explosionsList = []


def load_level_2():
	global sprite, bullets, obstaclesList, spikesList, powerUps, reloadBigShots
	global reloadFastShots, reloadDoubleShots, reloadTripleBullet
	global explosionsList, enemies, gameOver, flagRect, current_level

	pygame.mixer.music.pause()

	pygame.mixer.music.load('Data/level2.mp3')
	pygame.mixer.music.play(-1)

	#level2Music.play()
	

	current_level = 2
	sprite = player(0, display_dimensions[1] - 64, 40, 40,5)
	enemies = []
	bullets = []

	gameOver = False

	obstaclesList = createObstaclesLists(level_2_obstaclesPosList)

	spikesList = createSpikeLists(level_2_spikesPosList)

	flagRect = pygame.Rect(329, 34, 41, 60)
	powerUps = []
	# functional powerUp :
	# powerUps.append(largerBullet((221, 311)))
	powerUps.append(fasterBullet((25, 462)))
	powerUps.append(permaBuffSpeed((1108, 204)))
	powerUps.append(doubleBullet((615, 439)))
	powerUps.append(tripleBullet((791, 98)))


	reloadBigShots = 0
	reloadFastShots = 0
	reloadDoubleShots = 0
	reloadTripleBullet = 0

	explosionsList = []



load_level_1() # the user will begin at level X

while run:

	clock = pygame.time.Clock()
	pygame.display.update()
	pygame.time.delay(30)
	if current_level == 1:
		win.blit(background_level_1, (0, 0))
	elif current_level == 2:
		win.blit(background_level_2, (0, 0))


	for bullet in bullets:
		# Go through all bullet objects, and sees if the bullet is onscreen, then move it by its velocity across screen.
		if bullet.x < win.get_width() and bullet.x > 0:
			bullet.x += bullet.vel  # Moves the bullet by its vel
			# if we have picked up the triple bullet powerup, move the bullets up and down based.
			if reloadTripleBullet > 0:
				if bullet.upOrDown == 1:
					bullet.y += 2
				if bullet.upOrDown == 2:
					bullet.y -= 2
		else:
			bullets.pop(bullets.index(bullet))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	# check if the player collide with the spike
	if sprite.rect.colliderect(flagRect):
		if current_level == 1:
			print("you beat level 1....but there's more")
			load_level_2()
			continue
		elif current_level == 2:
			print("you won!!!  (congrats) ")
			


	# Check if the spikes hit the player
	for spike in spikesList:
		if spike.collide(sprite.rect):
			print("player dead")
			#remove spike that player collided with from screen
			spikesList.pop(spikesList.index(spike))
			 
			explosionsList.append(Explosion(sprite.rect.center))
			gameOver = True

	if gameOver: # make restart the level 1 when the user died
		if len(explosionsList) == 0: # if the explosions animations are finished

			dieSound.play()
			#restart music
			pygame.mixer.music.play(-1)
			
			load_level_1()
			continue


	# check if the bullets collide with :
		# a obstacle (platform)
	for bullet in bullets:
		for obstacle_rect in obstaclesList:
			if bullet.collide(obstacle_rect):
				print("bullet hit platfom -> destroy bullet")
				bullets.pop(bullets.index(bullet)) # remove the bullet

		# the spikes
	for bullet in bullets:
		for spike in spikesList:
			if bullet.collide(spike.rect):
				bullets.pop(bullets.index(bullet)) # remove the bullet
				spike.lives -= 1
				damage.play()
				if spike.lives <= 0: # if the spike has no more health
					explosionsList.append(Explosion(spike.rect.center))
					spikesList.pop(spikesList.index(spike)) # remove the spike
					explosionSound.play()
					print("bullet break spike")
					continue
				print("bullet hit spike")


	# make the explosions functional
	for explosion in explosionsList:
		explosion.draw()


	#Goes through all the powerup objects, and sees if a player hits the powerup. If the player hits the powerup hitbox, we
	#activate the powerup for that particular object
	for powerUp in powerUps:
		if powerUp.rect.colliderect(sprite.rect): # check if the powerUp collide with the sprite
			powerUp.activatePowerUp()
			powerup.play()


	keys = pygame.key.get_pressed()
	current_time = pygame.time.get_ticks()

	if keys[pygame.K_ESCAPE]:
		return_val = make_menu('pause')
	#time between shots when space is pressed
	if keys[pygame.K_SPACE] and current_time - previous_time > 300: # reload time
		previous_time = current_time
		shootNormalSound.play()
		

		if sprite.isLooking == "right":
			facing = 1
		else:
			facing = -1

		if len(bullets) < 100:
			# This will make sure we cannot exceed 100 bullets on the screen at once
			# ALl these if statements check if a powerup for projectiles was picked, and then
			# appends the appropriate projectile based on the powerup the sprite acquired.
			if reloadBigShots > 0:
				bullets.append(projectile(sprite.rect.centerx , sprite.rect.centery, 18, (0, 200, 0),facing,8))
				reloadBigShots -= 1
			elif reloadFastShots > 0:
				bullets.append(projectile(sprite.rect.centerx , sprite.rect.centery, 6,
											(0, 200, 0),facing, 16))
				reloadFastShots -= 1
			elif reloadDoubleShots > 0:
				bullets.append(projectile(sprite.rect.centerx+7 , sprite.rect.centery, 6,
												(0, 200, 0),facing, 8))

				bullets.append(projectile(sprite.rect.centerx-7, sprite.rect.centery, 6,
												(0, 200, 0), facing, 8))
				reloadDoubleShots -= 1

			elif reloadTripleBullet > 0:
				bullets.append(projectile(sprite.rect.centerx , sprite.rect.centery, 6,
											(0, 200, 0), facing, 8))
				bullets.append((projectile(sprite.rect.centerx , sprite.rect.centery, 6,
											(0, 200, 0), facing, 8,1)))
				bullets.append((projectile(sprite.rect.centerx , sprite.rect.centery, 6,
											(0, 200, 0), facing, 8,2)))
				reloadTripleBullet -= 1

			else: # classic bullets
				bullets.append(projectile(sprite.rect.centerx , sprite.rect.centery, 6, (0, 200, 0),
											facing,8))

	if not gameOver: # the slime player can move only if he is alive
		sprite.move()


	GameWindow()
pygame.quit()
