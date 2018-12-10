#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os
import blocks
import monsters
import sys
MOVE_SPEED = 7
WIDTH =35
HEIGHT = 46
COLOR =  "#888888"
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, яка тяне нас до низу
ANIMATION_DELAY = 0.1 # швидкість зміни
ICON_DIR = os.path.dirname(__file__) #  повний шлях до каталогу файлу

ANIMATION_RIGHT = [('%s/player/rightRun1.png' % ICON_DIR),
            ('%s/player/rightRun2.png' % ICON_DIR),
            ('%s/player/rightRun3.png' % ICON_DIR),
            ('%s/player/rightRun4.png' % ICON_DIR),
            ('%s/player/rightRun5.png' % ICON_DIR),
            ('%s/player/rightRun6.png' % ICON_DIR),
            ('%s/player/rightRun7.png' % ICON_DIR),
            ('%s/player/rightRun8.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/player/leftRun1.png' % ICON_DIR),
            ('%s/player/leftRun2.png' % ICON_DIR),
            ('%s/player/leftRun3.png' % ICON_DIR),
            ('%s/player/leftRun4.png' % ICON_DIR),
            ('%s/player/leftRun5.png' % ICON_DIR),
            ('%s/player/leftRun6.png' % ICON_DIR),
            ('%s/player/leftRun7.png' % ICON_DIR),
            ('%s/player/leftRun8.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/player/leftRun1.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/player/rightRun1.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/player/Idle.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/player/Idle.png' % ICON_DIR, 0.1)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #швидкість руху, 0 - стоїть на місці
        self.startX = x # Початкого позиція х
        self.startY = y
        self.yvel = 0 # швидкість вертикального переміщення
        self.onGround = False # чи я на землі?
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямокутний обєкт
        self.image.set_colorkey(Color(COLOR)) # робим фон прозорим
#        Анімація руху вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
#        Анімація руху вправо
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # По-замовчуванні , стоїмо
        
        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        #self.winner = False

    def update(self, left, right, up, platforms):
        
        if up:
            if self.onGround: # стрибаєм тільки тоді коли стоїмо на землі
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))
               
                       
        if left:
            self.xvel = -MOVE_SPEED # Лево = x- n
            self.image.fill(Color(COLOR))
            if up: # для стрибка вліво,анімація
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
 
        if right:
            self.xvel = MOVE_SPEED # Вправо = х +n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))
         
        if not(left or right): # Стоїмо,коли є вказівка
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
            
        if not self.onGround:
            self.yvel +=  GRAVITY
            
        self.onGround = False; # Ми не знаєм коли ми стоїмо
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свої координати xvel
        self.collide(self.xvel, 0, platforms)
   
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # якщо гравець пересікається з платформою
                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster):  # если пересакаемый блок - blocks.BlockDie или Monster
                    self.die()
                elif isinstance(p, blocks.Princess): # если коснулись принцессы
                       sys.exit() # победили!!!
                if xvel > 0:                      # якщо рухається вправо
                    self.rect.right = p.rect.left # якщо рухається вліво

                if xvel < 0:                      # якщо рухається вліво
                    self.rect.left = p.rect.right # якщо стоїть

                if yvel > 0:                      # якщо падає вниз
                    self.rect.bottom = p.rect.top # якщо не падає
                    self.onGround = True          # стоєм на щось тверду
                    self.yvel = 0                 # і енергія не падає

                if yvel < 0:                      # якщо рухаємся вверх
                    self.rect.top = p.rect.bottom # то не рухається вверх
                    self.yvel = 0                 # і енергія падає

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)  # перемещаемся в начальные координаты