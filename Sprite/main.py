import pygame
pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Game")
background = pygame.image.load('/Users/salpecoraro/Downloads/background.jpg')
rightSprite = pygame.image.load('/Users/salpecoraro/Downloads/SlimePreview-2.png')
leftSprite = pygame.image.load('/Users/salpecoraro/Downloads/image-2.png')

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
    win.blit(background,(0,0))
    #if walkCount + 1 >= 27
    if left:
        win.blit(leftSprite,(x,y))
        print("here")
    elif right:
        win.blit(rightSprite,(x,y))
    else:
        win.blit(rightSprite,(x,y))
    pygame.display.update()

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