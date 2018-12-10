#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os
import pyganim
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#87390b"
ICON_DIR = os.path.dirname(__file__) #  повний шлях до файлів

PRINCESS_WIDTH = 59
PRINCESS_HEIGHT = 90

ANIMATION_PRINCESS = [
    ('%s/blocks\princess_1.png' % ICON_DIR),
    ('%s/blocks/princess_2.png' % ICON_DIR)]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/dieBlock.png" % ICON_DIR)


class Princess(Platform):
    def __init__(self,PRINCESS_WIDTH,PRINCESS_HEIGHT):
        Platform.__init__(self, PRINCESS_WIDTH, PRINCESS_HEIGHT)
        boltAnim = []
        for anim in ANIMATION_PRINCESS:
            boltAnim.append((anim, 0.8))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))