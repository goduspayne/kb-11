#!/usr/bin/env python
# -*- coding: utf-8 -*-
#KB-11
# Импортируем библиотеку pygame
import pygame
from player import *
from blocks import *
from pygame import *
import sys

#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 600 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
screen_menu = pygame.Surface((800, 600))
info_menu = pygame.Surface((800, 600))


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)        


def main():
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Halloween Spirit") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
    
    hero = Player(65,650) # создаем героя по (x,y) координатам
    left = right = False # по умолчанию - стоим
    up = False
    
    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    
    entities.add(hero)
           
    level = [
       "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
       "-                                             -           -                                -                          -              -                                                             -",
       "-                                             -           -                                -                          -              -                                                             -",
       "--           ---                              ------      -             ----------         -                          -------        -                ------                                       -",
       "-                                                         -                                -                                         ----                -----                    ------------------",
       "-                                                         -                                -                                         -                   -------                  ------------------",
       "-                                     ----------------------------                         -                 ---                     -                   ---------                                 -",
       "--                                                        -                                ----              ---                     -                   -----------                               -",
       "-             -------------                               -                       ----------                                     -----             ------------------------                      ---",
       "-             -           -                               -                                -                                         -                   ------------------                    -----",
       "-             -           -           -------             --                               -                                         -                   -                                   -------",
       "-         -------         -                               -                                -          ---           ---              ----                -                                 ---------",
       "-         -               -                               -                --              -                                         -                   -                          ----------------",
       "--        -               -                         --------                               -                                         -                   -                          ----------------",
       "-         -               -                               -                                -                                    ------                   -                                         -",
       "-         -       ---------           -------             -                                -                                 ---------          -------------------                                -",
       "-         -                                               -                        --------------                      ---------------          -                                                  -",
       "----      -                                               -------              -----            ------                                          -                                                  -",
       "-         -                                                                                                                                     -                                                  -",
       "-        ---                                                                                                                                    -                                                  -",
       "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
        ]



    class Menu:
        def __init__(self, punkts=[400, 350, u'Punkt', (250, 250, 30), (250, 30, 250)]):
            self.punkts = punkts

        def render(self, poverhnost, font, num_punkt):
            for i in self.punkts:
                if num_punkt == i[5]:
                    poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
                else:
                    poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

        def menu(self):
            done = True
            pygame.font.init()
            font_menu = pygame.font.Font(None, 50)
            pygame.key.set_repeat(0, 0)
            pygame.mouse.set_visible(True)
            punkt = 0
            while done:
                menubg = pygame.image.load('backgrounds\BG_menu.jpg')
                info_menu.blit(menubg, (0, 0))
                screen_menu.blit(menubg, (0, 0))

                mp = pygame.mouse.get_pos()
                for i in self.punkts:
                    if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                        punkt = i[5]
                self.render(screen_menu, font_menu, punkt)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            sys.exit()
                        if e.key == pygame.K_UP:
                            if punkt > 0:
                                punkt -= 1
                        if e.key == pygame.K_DOWN:
                            if punkt < len(self.punkts) - 1:
                                punkt += 1
                        if e.key == pygame.K_p:
                            done = False
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        if punkt == 0:
                            done = False
                        elif punkt == 1:
                            exit()
                screen.blit(info_menu, (0, 0))
                screen.blit(screen_menu, (0, 30))
                pygame.display.flip()

    punkts = [(350, 300, u'Play', (11, 0, 77), (250, 250, 30), 0),
              (350, 340, u'Exit', (11, 0, 77), (250, 250, 30), 1)]
    game = Menu(punkts)
    game.menu()
    timer = pygame.time.Clock()
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту
    
    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1: # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                sys.exit(), "QUIT"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_p:
                game.menu()

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False


        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 


        camera.update(hero) # центризируем камеру относительно персонажа
        hero.update(left, right, up,platforms) # передвижение
        #entities.draw(screen) # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        
        
        pygame.display.update()     # обновление и вывод всех изменений на экран
        

if __name__ == "__main__":
    main()
