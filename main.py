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


class largerBullet(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)

    def activatePowerUp(self):
        global reloadBigShots
        reloadBigShots = 10
        powerUps.pop(powerUps.index(self))


class fasterBullet(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)

    def activatePowerUp(self):
        global reloadFastShots
        reloadFastShots = 10
        powerUps.pop(powerUps.index(self))


class fasterSlime(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)

    def activatePowerUp(self):
        global activateFastSlime, recordTimeWhileFastSlimeMode
        activateFastSlime = True
        recordTimeWhileFastSlimeMode = pygame.time.get_ticks()
        powerUps.pop(powerUps.index(self))

class permaBuffSpeed(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)

    def activatePowerUp(self):
        powerUps.pop(powerUps.index(self))
        sprite.vel = 7

class doubleBullet(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)

    def activatePowerUp(self):
        global reloadDoubleShots
        reloadDoubleShots = 10
        powerUps.pop(powerUps.index(self))

class tripleBullet(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)

    def activatePowerUp(self):
        global reloadTripleBullet
        reloadTripleBullet = 10
        powerUps.pop(powerUps.index(self))

class doubleJump(object):
    #does not work lol
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)


class gliding(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)

    def activatePowerUp(self):
        global activateGlideSlime, recordTimeWhileGlidingSlimeMode
        activateGlideSlime = True
        powerUps.pop(powerUps.index(self))


class projectile(object):
    def __init__(self, x, y, radius, color, facing, vel,upOrDown = 0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = vel * facing
        self. upOrDown = upOrDown


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x*scale, self.y*scale), self.radius*scale)


class enemy(object):
    # Blueprints to create enemy type objects
    fireImage = pygame.image.load('Data/Fire.jpg')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width * scale
        self.height = height * scale
        self.hitbox = (self.x, self.y, width, height)
        self.size = self.fireImage.get_size()
        self.health = 3
        self.dead = False


    def draw(self, win):
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.fireImage = pygame.transform.scale(self.fireImage, (int(self.size[0] * scale), int(self.size[1]) * scale))
        # change size of sprite
        win.blit(self.fireImage, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.health -= 1
        bullets.pop(bullets.index(bullet))
        if self.health == 0:
            self.dead = True
            print("DEAD")
            listOfSpikelists.append(createSpikeLists(self.x,self.y))
            enemies.pop(enemies.index(enemy))


def createSpikeLists(x,y):
    listOfSpikes = []
    listOfSpikes.append(spike(x, y, 0, 5))
    listOfSpikes.append(spike(x, y, 5, 5))
    listOfSpikes.append(spike(x, y, 5, 0))
    listOfSpikes.append(spike(x, y, 5, -5))
    listOfSpikes.append(spike(x, y, 0, -5))
    listOfSpikes.append(spike(x, y, -5, -5))
    listOfSpikes.append(spike(x, y, -5, 0))
    listOfSpikes.append(spike(x, y, -5, 5))
    return listOfSpikes


class spike(object):

    def __init__(self, x, y, xVel,yVel):
        self.northeastSpike = pygame.image.load('Data/Fire.jpg')
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.size = self.northeastSpike.get_size()
        self.hitbox = (x,y,self.size[0])

    def draw(self, win):
        self.hitbox = (self.x,self.y,self.size[0])
        self.northeastSpike = pygame.transform.scale(self.northeastSpike, (self.size[0], self.size[1]))
        win.blit(self.northeastSpike, (self.x, self.y))



class player(object):
    def __init__(self, x, y, width, height,vel):
        self.x = x
        self.y = y
        self.massGain = scale
        self.width = width
        self.height = height
        self.vel = vel
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.facing = True
        self.rightSprite = pygame.image.load('Data/rightSprite.png')
        self.defaultSprite = pygame.image.load('Data/rightSprite.png')
        self.leftSprite = pygame.image.load('Data/image-2.png')
        self.configure = 0
        self.health = 3

    def draw(self, win):
        tempWidth = int(self.width * self.massGain)
        win.blit(pygame.transform.scale(display, (display_dimensions[0] * scale, display_dimensions[1] * scale)),(0, 0))
        self.hitbox = (self.x * scale+self.configure, self.y * scale, tempWidth, tempWidth)
        if self.left:
            self.leftSprite = pygame.transform.scale(self.leftSprite,(tempWidth, tempWidth))
            win.blit(self.leftSprite, (self.x * scale+self.configure, self.y * scale))
            self.defaultSprite = pygame.image.load('Data/image-2.png')
            self.facing = False
        elif self.right:
            self.rightSprite = pygame.transform.scale(self.rightSprite,(tempWidth, tempWidth))
            win.blit(self.rightSprite, (self.x * scale+self.configure, self.y * scale))
            self.defaultSprite = pygame.image.load('Data/rightSprite.png')
            self.facing = True
        else:
            self.defaultSprite = pygame.transform.scale(self.defaultSprite,(tempWidth,tempWidth))
            win.blit(self.defaultSprite, (self.x * scale+self.configure, self.y * scale))
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class massPowerUp(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x * scale, self.y * scale), self.radius * scale)

    def activatePowerUp(self):
        sprite.massGain += .3
        sprite.y -= 6.4
        sprite.configure += 19.2
        global width
        width += 1
        sprite.health += 1
        powerUps.pop(powerUps.index(self))

previousTime = 0
def hit():
    currentTime = pygame.time.get_ticks()
    global previousTime
    # time between shots when space is pressed
    if currentTime - previousTime > 550:
        previousTime = currentTime
        sprite.health -= 1
        sprite.massGain -= .3
        sprite.configure -= 19.2
        sprite.y += 6.4
        global trueWidth
        trueWidth += 6.4


def GameWindow():
    sprite.draw(win)
    for powerUp in powerUps:
        powerUp.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for list in listOfSpikelists:
        for spike in list:
            spike.draw(win)
    pygame.display.update()


run_menu()
run = True
display.blit(background, (0, 0))
previous_time = pygame.time.get_ticks()

sprite = player(0, display_dimensions[1] - 64, 64, 64,5)
enemies = []
enemies.append(enemy(600, 456, 64, 64))
bullets = []

powerUps = []
# powerUps.append(largerBullet(0,  display_dimensions[1] - 64, 40, (0, 200, 0)))
# powerUps.append(fasterBullet(0,  display_dimensions[1], 40, (200, 200, 200)))
# powerUps.append(fasterSlime(300,  display_dimensions[1], 80, (000, 000, 200)))200
# powerUps.append(doubleBullet(0,  display_dimensions[1], 80, (000, 000, 200)))
# powerUps.append(tripleBullet(0,  display_dimensions[1], 80, (000, 000, 200)))
# powerUps.append(permaBuffSpeed(0,  display_dimensions[1], 80, (000, 000, 200)))
# powerUps.append(gliding(0, display_dimensions[1], 80, (000, 000, 200)))
# powerUps.append(massPowerUp(0,  display_dimensions[1], 80, (000, 000, 200)))
# powerUps.append(massPowerUp(0,  display_dimensions[1], 80, (000, 000, 200)))
# powerUps.append(massPowerUp(0,  display_dimensions[1], 80, (000, 000, 200)))


reloadBigShots = 0
reloadFastShots = 0
reloadDoubleShots = 0
reloadTripleBullet = 0

recordTimeWhileFastSlimeMode = 0
recordTimeWhileGlidingSlimeMode = 0
recordTimeUntilNextHitRegisters = 0

activateFastSlime = False
activateGlideSlime = False
tripleBulletUp = []
tripleBulletDown = []
listOfSpikelists = []

trueWidth = 0

while run:

    for list in listOfSpikelists:
        for spike in list:
            spike.x += spike.xVel
            spike.y += spike.yVel
            # print(spike.hitbox[0]-spike.hitbox[2])
            #
            # print(sprite.hitbox[0] > spike.hitbox[0] - spike.hitbox[2])
            if sprite.hitbox[0] < spike.hitbox[0] + spike.hitbox[2] and sprite.hitbox[0] + sprite.hitbox[2] > spike.hitbox[0]:
                if sprite.hitbox[1] < spike.hitbox[1] + spike.hitbox[2] and sprite.hitbox[1] + sprite.hitbox[3] > spike.hitbox[1]:
                    hit()

    clock = pygame.time.Clock()
    display.blit(background, (0, 0))
    pygame.display.update()
    pygame.time.delay(30)


    if activateFastSlime == True:
        if pygame.time.get_ticks() - recordTimeWhileFastSlimeMode < 20000:
            sprite.vel *= 2
            getTime = pygame.time.get_ticks()
        else:
            sprite.vel /= 2
            activateFastSlime = False
    else:
        fastSlimeTime = 0

    for bullet in bullets:
        # Go through all bullet objects, and sees if the bullet is onscreen, then move it by its velocity across screen.
        if bullet.x < 500 and bullet.x > 0:

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
    #We go through all the enemy objects and sees if it hits a sprite.
    for enemy in enemies:
        if sprite.hitbox[0] > enemy.hitbox[0] - enemy.hitbox[2] and sprite.hitbox[0] - sprite.hitbox[2] < enemy.hitbox[0]:
            if sprite.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and sprite.hitbox[1] + sprite.hitbox[3] > enemy.hitbox[1]:
                hit()
    #We go through all the bullet objects currently on screen. We then go through all the enemy objects and sees if the
    #bullet hits any of the enemy objects. If a projectile hits a enemy, activate the enemy.hit()
    for bullet in bullets:
        for enemy in enemies:
            if bullet.y * scale - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y * scale + bullet.radius > enemy.hitbox[1]:
                if bullet.x*scale + bullet.radius > enemy.hitbox[0] and bullet.x *scale- bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                    enemy.hit()
    #Goes through all the powerup objects, and sees if a player hits the powerup. If the player hits the powerup hitbox, we
    #activate the powerup for that particular object
    for powerUp in powerUps:
        if powerUp.y * scale - powerUp.radius * scale < sprite.hitbox[1] + sprite.hitbox[3] and powerUp.y * scale + powerUp.radius *scale> sprite.hitbox[1]:
            if powerUp.x * scale + powerUp.radius *scale > sprite.hitbox[0] and powerUp.x * scale - powerUp.radius *scale < sprite.hitbox[0] + sprite.hitbox[2]:
                powerUp.activatePowerUp()

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    #time between shots when space is pressed
    width = sprite.width - trueWidth
    if keys[pygame.K_SPACE] and current_time - previous_time > 210:
        previous_time = current_time
        if sprite.facing:
            facing = 1
        else:
            facing = -1

        if len(bullets) < 100:


            # This will make sure we cannot exceed 5 bullets on the screen at once
            #ALl these if statements check if a powerup for projectiles was picked, and then
            #appends the appropriate projectile based on the powerup the sprite acquired.
            if reloadBigShots > 0:
                bullets.append(projectile(round(sprite.x + width // 2), round(sprite.y + width// 2), 12,(0, 200, 0),facing,8))
                reloadBigShots -= 1
            elif reloadFastShots > 0:
                bullets.append(projectile(round(sprite.x + width// 2), round(sprite.y + width // 2), 6,
                (0, 200, 0),facing, 16))
                reloadFastShots -= 1
            elif reloadDoubleShots > 0:
                bullets.append(projectile(round(sprite.x + width // 2), round(sprite.y + width // 2), 6,
                (0, 200, 0),facing, 8))
                if sprite.facing is False:
                    bullets.append(projectile(round(sprite.x + width // 2) - 20, round(sprite.y + width // 2), 6,
                    (0, 200, 0), facing, 8))
                else:
                    bullets.append(projectile(round(sprite.x + width // 2) + 20, round(sprite.y + width// 2), 6,
                    (0, 200, 0), facing, 8))
                reloadDoubleShots -= 1
            elif reloadTripleBullet > 0:
                bullets.append(projectile(round(sprite.x + width // 2) , round(sprite.y + width // 2), 6,
                (0, 200, 0), facing, 8))
                bullets.append((projectile(round(sprite.x + width // 2) , round(sprite.y + width // 2), 6,
                (0, 200, 0), facing, 8,1)))
                bullets.append((projectile(round(sprite.x + width // 2) , round(sprite.y + width // 2), 6,
                (0, 200, 0), facing, 8,2)))
                reloadTripleBullet -= 1
            else:
                bullets.append(projectile(round(sprite.x + width// 2), round(sprite.y + width// 2), 6, (0, 200, 0),
                facing,8))


    if keys[pygame.K_LEFT] and sprite.x + sprite.configure/3 > 0:
        sprite.x -= sprite.vel
        sprite.left = True
        sprite.right = False
    elif keys[pygame.K_RIGHT] and sprite.x + sprite.configure/3 < display_dimensions[0] - width - sprite.vel:
        print(width,sprite.x)
        sprite.x += sprite.vel
        sprite.left = False
        sprite.right = True
    else:
        sprite.right = False
        sprite.left = False
        sprite.walkCount = 0
    if not (sprite.isJump):
        if keys[pygame.K_UP]:
            sprite.isJump = True
            sprite.walkCount = 0
    else:
        if sprite.jumpCount >= -10:
            neg = 1
            if sprite.jumpCount < 0:
                neg = -1
            if neg == 1:
                sprite.y -= (sprite.jumpCount ** 2) * .5 * neg
            if neg == -1 and keys[pygame.K_g] and activateGlideSlime == True:
                sprite.y -= 3 * neg
                sprite.jumpCount = -1
            elif neg == -1:
                sprite.y -= (sprite.jumpCount ** 2) * .5 * neg
            sprite.jumpCount -= 1

        else:
            sprite.isJump = False
            sprite.jumpCount = 10

    GameWindow()
pygame.quit()

