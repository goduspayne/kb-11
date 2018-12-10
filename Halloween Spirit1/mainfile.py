#!/usr/bin/env python
# -*- coding: utf-8 -*-
# KB-111
# Импортируем библиотеку pygame
import pygame
from player import *
from blocks import *
import pyglet
from monsters import *


# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 600  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND = pygame.image.load('backgrounds\BGLVL1.jpg')
screen_menu = pygame.Surface((800, 600))
info_menu = pygame.Surface((800, 600))



FILE_DIR = os.path.dirname(__file__)

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
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel():
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя

    levelFile = open('%s/levels/1.txt' % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"

        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "player":  # если первая команда - player
                    playerX = int(commands[1])  # то записываем координаты героя
                    playerY = int(commands[2])
                if commands[0] == "monster":  # если первая команда monster, то создаем монстра
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                    int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)


def main():
    loadLevel()
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Halloween Spirit")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.blit(BACKGROUND,(0,0))  # Заливаем поверхность сплошным цветом

    hero = Player(playerX, playerY)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False


    entities.add(hero)
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    timer = pygame.time.Clock()

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

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



    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
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
            if e.type == KEYDOWN and e.key == K_b:
                main()

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        animatedEntities.update()  # показываеaм анимацию
        monsters.update(platforms)  # передвигаем всех монстров
        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # обновление и вывод всех изменений на экран


level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group() # Все передвигающиеся объекты
platforms = [] # то, во что мы будем врезаться или опираться
if __name__ == "__main__":
    main()

