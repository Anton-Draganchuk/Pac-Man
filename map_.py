from Data import *
import pygame
import numpy as np


class Map:
    def __init__(self, screen, image):
        """
        Инициализация объекта
        :param screen: Экран на котором происходит прорисовка карты
        :param image: Картинка игровой карты
        """
        self.number_map = np.zeros((33, 28), dtype=np.int64)
        self.font = pygame.font.Font(None, 20)
        self.Screen2 = pygame.Surface((560, 660))
        self.screen = screen
        self.image = image

    def walls(self, interface, pacman):
        """
        Определяет стенки, через которые неальзя проходить, и создает массив карты
        :param interface: Объект одноименного класса
        :param pacman: Объект одноименного класса
        :return: Изменяет наполнение массива исходя из того, что персонаж съедает еду
        """
        p = 1
        for j in range(28):
            for i in range(31):
                for x in range(j * interface.square_size, (j + 1) * interface.square_size):
                    for y in range(i * interface.square_size, (i + 1) * interface.square_size):
                        if self.image.get_at((x, y)) != (0, 0, 0, 0):
                            p *= 0
                if p == 0:
                    self.number_map[i, j] = 1
                    p = 1
                elif 7 <= j <= 20 and 9 <= i <= 19:
                    self.number_map[i, j] = 3
                elif i == 14 and (0 <= j <= 5 or 22 <= j <= 27):
                    self.number_map[i, j] = 3
                if (11 <= j <= 16 and i == 14) or (13 <= j <= 14 and 12 <= i <= 13):
                    self.number_map[i, j] = 3
        self.number_map[pacman.number_y, pacman.number_x] = 3
        self.number_map[pacman.number_y, pacman.number_x - 1] = 3


class Award:
    def __init__(self, screen):
        """
        Инициализация объекта
        :param screen: Экран на котором происходить прорисовка еды и фруктов
        """
        self.screen = screen
        self.score = 0
        self.screen2 = pygame.Surface((560, 660))
        self.time = 600
        self.fruit = 0
        self.fruit_time = 0
        self.factor = 1

    def draw_dot(self, card):
        """
        Функция которая рисует еду в тех местах где значения массива 0
        :param card: Карта в виде массива
        :return: Рисует квадратики
        """
        self.screen2.fill(BLACK)
        for j in range(28):
            for i in range(31):
                if card.number_map[i, j] == 0:
                    pygame.draw.rect(self.screen2, PINK, [j * 20 + 7, i * 20 + 7, 6, 6])

    def set_fruit(self, card):
        """
        Функция которая расставляет фрукты на карте, по определенному правилу
        :param card: Карта в виде массива
        :return: Добавляет в массив значение 4, обозначающее положение фрукта
        """
        i, j = 0, 0
        if self.time == 0 and (card.number_map == 4).sum() == 0:
            while card.number_map[i, j] != 0 and self.fruit < 3:
                i = np.random.randint(0, 31)
                j = np.random.randint(0, 28)
            card.number_map[i, j] = 4
            self.fruit += 1
        else:
            self.time -= 1

    def update(self, card, pacman):
        """
        Функция обновления, которая считывает съедена еда или нет, реализует эффект фруктов
        :param card: Карта в виде массива
        :param pacman: Объект одноименного класса
        :return: Изменяет колличество очков
        """
        if card.number_map[pacman.number_y, pacman.number_x] == 0:
            self.score += 10 * self.factor
        elif card.number_map[pacman.number_y, pacman.number_x] == 4:
            self.fruit_time = 300
            self.time = np.random.randint(800, 1200)
        card.number_map[pacman.number_y, pacman.number_x] = 3

        if self.fruit_time != 0:
            self.factor = 10
            self.fruit_time -= 1
        else:
            self.factor = 1

    def draw_fruit(self, card, Fruit):
        """
        Функция рисования фруктов по определенному правилу
        :param card: Карта в виде массива
        :param Fruit: Список из всех фруктов
        :return: Рисует фрукты на карте и внизу экрана
        """
        self.set_fruit(card)

        for j in range(28):
            for i in range(31):
                if self.fruit < 4 and card.number_map[i, j] == 4:
                    self.screen2.blit(Fruit[self.fruit - 1], (j * 20, i * 20))

        if (card.number_map == 4).sum() == 0:
            for f in range(self.fruit):
                self.screen2.blit(pygame.transform.scale(Fruit[f], (40, 40)),
                                  ((28 - 2 * self.fruit + 2 * f) * 20, 31 * 20))
        else:
            for f in range(self.fruit - 1):
                self.screen2.blit(pygame.transform.scale(Fruit[f], (40, 40)),
                                  ((28 - 2 * self.fruit + 2 + 2 * f) * 20, 31 * 20))

        self.screen2.set_colorkey(BLACK)
        self.screen.blit(self.screen2, (0, 60))

