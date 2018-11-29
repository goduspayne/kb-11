import pygame
from pygame import *

pygame.init()
win = pygame.display.set_mode((800,600))

pygame.display.set_caption("Halloween Spirit")

level = [
       "-------------------------",
       "                       ",
       "                       ",
       "                       ",
       "            --         ",
       "                       ",
       "--                     ",
       "                       ",
       "                   --- ",
       "                       ",
       "                       ",
       "      ---              ",
       "                       ",
       "                       ",
       "                   ---- ",
       "                       ",
       "                       ",
       "                       ",
       "                       ",]



walkRight = [pygame.image.load('img\Run (1).png'),pygame.image.load('img\Run (2).png'),
             pygame.image.load('img\Run (3).png'),pygame.image.load('img\Run (4).png'),
             pygame.image.load('img\Run (5).png'),pygame.image.load('img\Run (6).png'),
             pygame.image.load('img\Run (7).png'),pygame.image.load('img\Run (8).png'),
             pygame.image.load('img\Run (1).png')]

walkLeft = [pygame.image.load('img\leftRun1.png'),pygame.image.load('img\leftRun2.png'),
            pygame.image.load('img\leftRun3.png'),pygame.image.load('img\leftRun4.png'),
            pygame.image.load('img\leftRun5.png'),pygame.image.load('img\leftRun6.png'),
            pygame.image.load('img\leftRun7.png'),pygame.image.load('img\leftRun8.png'),
            pygame.image.load('img\leftRun1.png')]

bg = pygame.image.load('img\BG.png')
playerStand = pygame.image.load('img\Idle (2).png')

clock = pygame.time.Clock()



x = 50
y = 460
widht = 70
height = 92
speed = 5

left = False
right = False
animCount = 0

isJump = False
jumpCount = 10


def drawWindow():
    global animCount
    win.blit(bg,(0,0))

    if animCount + 1 >= 30:
        animCount = 0
    if right:
        win.blit(walkRight[animCount // 6], (x, y))
        animCount += 1
    elif left:
        win.blit(walkLeft[animCount // 6],(x,y))
        animCount += 1
    else:
        win.blit(playerStand, (x, y))

    pygame.display.update()


    z = h = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                # создаем блок, заливаем его цветом и рисеум его
                pf = Surface((32,32))
                pf.fill(Color("#FF6262"))
                bg.blit(pf, (z, h))

            z += 32  # блоки платформы ставятся на ширине блоков
        h += 32  # то же самое и с высотой
        z = 0  # на каждой новой строчке начинаем с нуля

#основний цикл
run = True
while run:


    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 800 - widht - 5:
        x += speed
        left = False
        right = True
    else:
        left = False
        right = False
        animCount = 0
    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            if jumpCount < 0:
                y += (jumpCount ** 2) / 2
            else:
                y -= (jumpCount ** 2) / 2
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10





    drawWindow()

pygame.quit()

