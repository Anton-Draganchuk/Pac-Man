import numpy as np
import pygame


class GhostRed(pygame.sprite.Sprite):
    def __init__(self, image):
        """
        Инициализация объекта
        :param image: Список картинок призрака
        """
        pygame.sprite.Sprite.__init__(self)
        self.picture = image
        self.image = self.picture[0]
        self.rect = self.image.get_rect()
        self.rect.center = 280, 290
        self.speed = 1
        self.speedx = self.speed
        self.speedy = 0
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))
        self.dist_left = 0
        self.dist_right = 0
        self.dist_up = 0
        self.dist_down = 0
        self.mode = 1
        self.time = 0
        self.time_hunter = 960
        self.time_relax = 560
        self.distance = []

    def distance2_pacman(self, x, y):
        """
        Функция расчета координаты текущего положения и растояния до целевой клетки
        :param x: Координата целевой клетки
        :param y: Координата целевой клетки
        :return: Значение расстояния
        """
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))
        self.dist_left = np.sqrt((self.left - x) ** 2 + (self.number_y - y) ** 2)
        self.dist_right = np.sqrt((self.right - x) ** 2 + (self.number_y - y) ** 2)
        self.dist_up = np.sqrt((self.number_x - x) ** 2 + (self.up - y) ** 2)
        self.dist_down = np.sqrt((self.number_x - x) ** 2 + (self.down - y) ** 2)
        self.distance = [self.dist_left, self.dist_right, self.dist_up, self.dist_down]

    def set_mode(self):
        """
        Функция выбора режима движения
        :return: Присваивает значения режима
        """
        if self.time <= self.time_relax:
            self.mode = 2
        elif self.time <= self.time_relax + self.time_hunter:
            self.mode = 1
        else:
            self.time = 0
        self.time += 1

    def mode1(self, Pacman, map):
        """
        Функция описывает первый режим
        :param Pacman: Объект одноименного класса
        :param map: Объект одноименного класса, с игровым массивом
        :return: Движение призрака
        """
        self.way(map, Pacman.number_x, Pacman.number_y)

    def mode2(self, map):
        """
        Функция описывает второй режим
        :param map: Объект одноименного класса, игровой массив
        :return: Движение призрака
        """
        self.way(map, 27, -2)

    def way(self, map, x, y):
        """
        Функция движения призрака к целевой точке
        :param map: Объект одноименного класса, игровой массив
        :param x: Координата целевой точки
        :param y: Координата целевой точки
        :return: Движение объекта
        """
        # Получаем значения вокруг призрака, с 4 сторон
        self.distance2_pacman(x, y)

        # Перемещение призрака
        if self.speedx > 0:
            self.distance.remove(self.dist_left)
        elif self.speedx < 0:
            self.distance.remove(self.dist_right)
        elif self.speedy > 0:
            self.distance.remove(self.dist_up)
        elif self.speedy < 0:
            self.distance.remove(self.dist_down)
        if map.number_map[self.up, self.number_x] == 1:
            self.distance.remove(self.dist_up)
        if map.number_map[self.down, self.number_x] == 1:
            self.distance.remove(self.dist_down)
        if map.number_map[self.number_y, self.left] == 1:
            self.distance.remove(self.dist_left)
        if map.number_map[self.number_y, self.right] == 1:
            self.distance.remove(self.dist_right)
        if self.down == 12 and 13 <= self.number_x <= 14 and self.speedy == 0:
            self.distance.remove(self.dist_down)

        if not self.distance:
            self.speedx = 0
            self.speedy = 0
        else:
            if self.dist_up <= min(self.distance) and \
                    self.speedy <= 0 and map.number_map[self.up, self.number_x] != 1:
                self.speedy = - self.speed
                self.speedx = 0
            elif self.dist_down <= min(self.distance) and \
                    self.speedy >= 0 and map.number_map[self.down, self.number_x] != 1:
                self.speedy = self.speed
                self.speedx = 0
            elif self.dist_left <= min(self.distance) and \
                    self.speedx <= 0 and map.number_map[self.number_y, self.left] != 1:
                self.speedy = 0
                self.speedx = - self.speed
            elif self.dist_right <= min(self.distance) and \
                    self.speedx >= 0 and map.number_map[self.number_y, self.right] != 1:
                self.speedy = 0
                self.speedx = self.speed

    def update(self, Pacman, map, award):
        """
        Функция обновления координаты объекта
        :param Pacman: Объект одноименного класса
        :param map: Объект одноименного класса, игровой массив
        :param award: Объект одноименного класса
        :return: Присваевает новую координату и изменяет скорость объекта, поворот
        """
        # Установить режим с помощью таймера time
        self.set_mode()

        # Перемещение призрака
        if self.rect.centerx % 20 == 10 and self.rect.centery % 20 == 10:
            if self.mode == 1:
                self.mode1(Pacman, map)
            elif self.mode == 2:
                self.mode2(map)

        # Перемещение на значение его скорости
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Прохождение через тунель
        if self.rect.centerx < 9:
            self.rect.centerx = 540
        elif self.rect.centerx > 549:
            self.rect.centerx = 10

        # Выбор картинки по направлению
        if self.speedx < 0:
            self.image = self.picture[0]
        elif self.speedx > 0:
            self.image = self.picture[2]
        elif self.speedy > 0:
            self.image = self.picture[3]
        elif self.speedy < 0:
            self.image = self.picture[1]


class GhostPink(pygame.sprite.Sprite):
    def __init__(self, image):
        """
        Инициализация объекта
        :param image: Список картинок призрака
        """
        pygame.sprite.Sprite.__init__(self)
        self.picture = image
        self.image = self.picture[0]
        self.rect = self.image.get_rect()
        self.rect.center = 290, 350
        self.speed = 1
        self.speedx = 0
        self.speedy = 0
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))
        self.dist_left = 0
        self.dist_right = 0
        self.dist_up = 0
        self.dist_down = 0
        self.mode = -1
        self.time = 0
        self.time_hunter = 960
        self.time_relax = 560
        self.distance = []

    def distance2_pacman(self, x, y):
        """
        Функция расчета координаты текущего положения и растояния до целевой клетки
        :param x: Координата целевой клетки
        :param y: Координата целевой клетки
        :return: Значение расстояния
        """
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))
        self.dist_left = np.sqrt((self.left - x) ** 2 + (self.number_y - y) ** 2)
        self.dist_right = np.sqrt((self.right - x) ** 2 + (self.number_y - y) ** 2)
        self.dist_up = np.sqrt((self.number_x - x) ** 2 + (self.up - y) ** 2)
        self.dist_down = np.sqrt((self.number_x - x) ** 2 + (self.down - y) ** 2)
        self.distance = [self.dist_left, self.dist_right, self.dist_up, self.dist_down]

    def set_mode(self, award):
        """
        Функция выбора режима движения
        :return: Присваивает значения режима
        """
        if award.score > 1000:
            if (11 <= self.number_x <= 16 and self.number_y == 14) or \
                    (13 <= self.number_x <= 14 and 12 <= self.number_y <= 13):
                self.mode = 0
            elif self.time <= self.time_relax:
                self.mode = 2
            elif self.time <= self.time_relax + self.time_hunter:
                self.mode = 1
            else:
                self.time = 0
            self.time += 1

    def mode0(self, map):
        """
        Функция описывает нулевой режим
        :param map: Объект одноименного класса, игровой массив
        :return: Движение призрака
        """
        self.way(map, 2, -2)

    def mode1(self, Pacman, map):
        """
        Функция описывает первый режим
        :param Pacman: Объект одноименного класса
        :param map: Объект одноименного класса, с игровым массивом
        :return: Движение призрака
        """
        self.way(map, Pacman.number_x, Pacman.number_y)

    def mode2(self, map):
        """
        Функция описывает второй режим
        :param map: Объект одноименного класса, игровой массив
        :return: Движение призрака
        """
        self.way(map, 2, -2)

    def way(self, map, x, y):
        """
        Функция движения призрака к целевой точке
        :param map: Объект одноименного класса, игровой массив
        :param x: Координата целевой точки
        :param y: Координата целевой точки
        :return: Движение объекта
        """
        # Получаем значения вокруг призрака, с 4 сторон
        self.distance2_pacman(x, y)

        # Перемещение призрака
        if self.speedx > 0:
            self.distance.remove(self.dist_left)
        elif self.speedx < 0:
            self.distance.remove(self.dist_right)
        elif self.speedy > 0:
            self.distance.remove(self.dist_up)
        elif self.speedy < 0:
            self.distance.remove(self.dist_down)
        if map.number_map[self.up, self.number_x] == 1:
            self.distance.remove(self.dist_up)
        if map.number_map[self.down, self.number_x] == 1:
            self.distance.remove(self.dist_down)
        if map.number_map[self.number_y, self.left] == 1:
            self.distance.remove(self.dist_left)
        if map.number_map[self.number_y, self.right] == 1:
            self.distance.remove(self.dist_right)

        if not self.distance:
            self.speedx = 0
            self.speedy = 0
        else:
            if self.dist_up <= min(self.distance) and \
                    self.speedy <= 0 and map.number_map[self.up, self.number_x] != 1:
                self.speedy = - self.speed
                self.speedx = 0
            elif self.dist_down <= min(self.distance) and \
                    self.speedy >= 0 and map.number_map[self.down, self.number_x] != 1:
                self.speedy = self.speed
                self.speedx = 0
            elif self.dist_left <= min(self.distance) and \
                    self.speedx <= 0 and map.number_map[self.number_y, self.left] != 1:
                self.speedy = 0
                self.speedx = - self.speed
            elif self.dist_right <= min(self.distance) and \
                    self.speedx >= 0 and map.number_map[self.number_y, self.right] != 1:
                self.speedy = 0
                self.speedx = self.speed

    def update(self, Pacman, Map, award):
        """
        Функция обновления координаты объекта
        :param Pacman: Объект одноименного класса
        :param Map: Объект одноименного класса, игровой массив
        :param award: Объект одноименного класса
        :return: Присваевает новую координату и изменяет скорость объекта, поворот
        """
        # Установить режим с помощью таймера time
        self.set_mode(award)

        # Перемещение призрака
        if self.rect.centerx % 20 == 10 and self.rect.centery % 20 == 10:
            if self.mode == 0:
                self.mode0(Map)
            elif self.mode == 1:
                self.mode1(Pacman, Map)
            elif self.mode == 2:
                self.mode2(Map)

        # Перемещение на значение его скорости
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Прохождение через тунель
        if self.rect.centerx < 9:
            self.rect.centerx = 540
        elif self.rect.centerx > 549:
            self.rect.centerx = 10

        # Выбор картинки по направлению
        if self.speedx < 0:
            self.image = self.picture[0]
        elif self.speedx > 0:
            self.image = self.picture[2]
        elif self.speedy > 0:
            self.image = self.picture[3]
        elif self.speedy < 0:
            self.image = self.picture[1]


class GhostBlue(pygame.sprite.Sprite):
    def __init__(self, image):
        """
        Инициализация объекта
        :param image: Список картинок призрака
        """
        pygame.sprite.Sprite.__init__(self)
        self.picture = image
        self.image = self.picture[0]
        self.rect = self.image.get_rect()
        self.rect.center = 250, 350
        self.speed = 1
        self.speedx = 0
        self.speedy = 0
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))
        self.dist_left = 0
        self.dist_right = 0
        self.dist_up = 0
        self.dist_down = 0
        self.mode = -1
        self.time = 0
        self.time_hunter = 960
        self.time_relax = 560
        self.distance = []

    def distance2_pacman(self, x, y):
        """
        Функция расчета координаты текущего положения и растояния до целевой клетки
        :param x: Координата целевой клетки
        :param y: Координата целевой клетки
        :return: Значение расстояния
        """
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))
        self.dist_left = np.sqrt((self.left - x) ** 2 + (self.number_y - y) ** 2)
        self.dist_right = np.sqrt((self.right - x) ** 2 + (self.number_y - y) ** 2)
        self.dist_up = np.sqrt((self.number_x - x) ** 2 + (self.up - y) ** 2)
        self.dist_down = np.sqrt((self.number_x - x) ** 2 + (self.down - y) ** 2)
        self.distance = [self.dist_left, self.dist_right, self.dist_up, self.dist_down]

    def set_mode(self, award):
        """
        Функция выбора режима движения
        :return: Присваивает значения режима
        """
        if award.score > 1010:
            if (11 <= self.number_x <= 16 and self.number_y == 14) or \
                    (13 <= self.number_x <= 14 and 12 <= self.number_y <= 13):
                self.mode = 0
            elif self.time <= self.time_relax:
                self.mode = 2
            elif self.time <= self.time_relax + self.time_hunter:
                self.mode = 1
            else:
                self.time = 0
            self.time += 1

    def mode0(self, map):
        """
        Функция описывает нулевой режим
        :param map: Объект одноименного класса, игровой массив
        :return: Движение призрака
        """
        self.way(map, 2, -2)

    def mode1(self, Pacman, map):
        """
        Функция описывает первый режим
        :param Pacman: Объект одноименного класса
        :param map: Объект одноименного класса, с игровым массивом
        :return: Движение призрака
        """
        self.way(map, Pacman.number_x, Pacman.number_y)

    def mode2(self, map):
        """
        Функция описывает второй режим
        :param map: Объект одноименного класса, игровой массив
        :return: Движение призрака
        """
        self.way(map, 28, 33)

    def way(self, map, x, y):
        """
        Функция движения призрака к целевой точке
        :param map: Объект одноименного класса, игровой массив
        :param x: Координата целевой точки
        :param y: Координата целевой точки
        :return: Движение объекта
        """
        # Получаем значения вокруг призрака, с 4 сторон
        self.distance2_pacman(x, y)

        # Перемещение призрака
        if self.speedx > 0:
            self.distance.remove(self.dist_left)
        elif self.speedx < 0:
            self.distance.remove(self.dist_right)
        elif self.speedy > 0:
            self.distance.remove(self.dist_up)
        elif self.speedy < 0:
            self.distance.remove(self.dist_down)
        if map.number_map[self.up, self.number_x] == 1:
            self.distance.remove(self.dist_up)
        if map.number_map[self.down, self.number_x] == 1:
            self.distance.remove(self.dist_down)
        if map.number_map[self.number_y, self.left] == 1:
            self.distance.remove(self.dist_left)
        if map.number_map[self.number_y, self.right] == 1:
            self.distance.remove(self.dist_right)

        if not self.distance:
            self.speedx = 0
            self.speedy = 0
        else:
            if self.dist_up <= min(self.distance) and \
                    self.speedy <= 0 and map.number_map[self.up, self.number_x] != 1:
                self.speedy = - self.speed
                self.speedx = 0
            elif self.dist_down <= min(self.distance) and \
                    self.speedy >= 0 and map.number_map[self.down, self.number_x] != 1:
                self.speedy = self.speed
                self.speedx = 0
            elif self.dist_left <= min(self.distance) and \
                    self.speedx <= 0 and map.number_map[self.number_y, self.left] != 1:
                self.speedy = 0
                self.speedx = - self.speed
            elif self.dist_right <= min(self.distance) and \
                    self.speedx >= 0 and map.number_map[self.number_y, self.right] != 1:
                self.speedy = 0
                self.speedx = self.speed

    def update(self, Pacman, Map, award):
        """
        Функция обновления координаты объекта
        :param Pacman: Объект одноименного класса
        :param Map: Объект одноименного класса, игровой массив
        :param award: Объект одноименного класса
        :return: Присваевает новую координату и изменяет скорость объекта, поворот
        """
        # Установить режим с помощью таймера time
        self.set_mode(award)

        # Перемещение призрака
        if self.rect.centerx % 20 == 10 and self.rect.centery % 20 == 10:
            if self.mode == 0:
                self.mode0(Map)
            elif self.mode == 1:
                self.mode1(Pacman, Map)
            elif self.mode == 2:
                self.mode2(Map)

        # Перемещение на значение его скорости
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Прохождение через тунель
        if self.rect.centerx < 9:
            self.rect.centerx = 540
        elif self.rect.centerx > 549:
            self.rect.centerx = 10

        # Выбор картинки по направлению
        if self.speedx < 0:
            self.image = self.picture[0]
        elif self.speedx > 0:
            self.image = self.picture[2]
        elif self.speedy > 0:
            self.image = self.picture[3]
        elif self.speedy < 0:
            self.image = self.picture[1]

