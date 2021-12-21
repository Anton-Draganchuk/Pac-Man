import numpy as np
import pygame


class Pacman(pygame.sprite.Sprite):
    def __init__(self, image):
        """
        Инициализация объекта
        :param image: Список из картинок персонажа, повернутого во все 4 стороны
        """
        pygame.sprite.Sprite.__init__(self)
        self.an = 0
        self.picture = image
        self.image = pygame.transform.rotate(self.picture[1], self.an)
        self.rect = self.image.get_rect()
        self.rect.center = 280, 530
        self.speedx = 0
        self.speedy = 0
        self.speed = 2
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))
        self.flag_left = 0
        self.flag_right = 0
        self.flag_up = 0
        self.flag_down = 0
        self.time2_turn = 20
        self.number_picture = 1
        self.time_image = 15

    def location(self):
        """
        Определяет текущую позицию и позицию со всех 4 сторон в виде отображения на массив с картой
        :return: Координаты текущего положения и соедних
        """
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))

    def update(self, pacman, map, award):
        """
        Обновление позициии за счет нажатия клавиш
        :param pacman: Объект одноименного класса
        :param map: Объект одноименного класса, используется для определения препятствий на пути
        :param award: Объект одноименного класса, используется для считывания вознаграждения
        :return: Изменение скорости объекта и совершение поворотов
        """
        # Получаем значения вокруг пакмена, с 4 сторон
        self.location()

        # Поворот с режимом залипания клавиши на колличество ходов time2_turn
        # Поворот налево
        keystore = pygame.key.get_pressed()
        if keystore[pygame.K_LEFT] or keystore[pygame.K_a] or self.flag_left > 0:
            if map.number_map[self.number_y, self.left] != 1 and self.rect.centery % 20 == 10:
                self.speedx = -self.speed
                self.an = 90
                self.speedy = 0
                self.flag_left = 0
            elif self.flag_left == 0:
                self.flag_left = self.time2_turn
            else:
                self.flag_left -= 1

        # Поворот на право
        elif keystore[pygame.K_RIGHT] or keystore[pygame.K_d] or self.flag_right > 0:
            if map.number_map[self.number_y, self.right] != 1 and self.rect.centery % 20 == 10:
                self.speedx = self.speed
                self.an = -90
                self.speedy = 0
                self.flag_right = 0
            elif self.flag_right == 0:
                self.flag_right = self.time2_turn
            else:
                self.flag_right -= 1

        # Поворот вверх
        elif keystore[pygame.K_UP] or keystore[pygame.K_w] or self.flag_up > 0:
            if map.number_map[self.up, self.number_x] != 1 and self.rect.centerx % 20 == 10:
                self.speedy = -self.speed
                self.an = 0
                self.speedx = 0
                self.flag_up = 0
            elif self.flag_up == 0:
                self.flag_up = self.time2_turn
            else:
                self.flag_up -= 1

        # Поворот вниз
        elif keystore[pygame.K_DOWN] or keystore[pygame.K_s] or self.flag_down > 0:
            if map.number_map[self.down, self.number_x] != 1 and self.rect.centerx % 20 == 10:
                self.speedy = self.speed
                self.an = 180
                self.speedx = 0
                self.flag_down = 0
            elif self.flag_down == 0:
                self.flag_down = self.time2_turn
            else:
                self.flag_down -= 1

        # Анимация пакмена
        self.view_image()

        # Если пакмен доходит до препятствия, он останавливается
        if self.speedy == -self.speed and map.number_map[self.up, self.number_x] == 1:
            self.speedy = 0
        if self.speedy == self.speed and map.number_map[self.down, self.number_x] == 1:
            self.speedy = 0
        if self.speedx == -self.speed and map.number_map[self.number_y, self.left] == 1:
            self.speedx = 0
        if self.speedx == self.speed and map.number_map[self.number_y, self.right] == 1:
            self.speedx = 0

        # Перемещение на значение его скорости
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Прохождение через тунель
        if self.rect.centerx < 9:
            self.rect.centerx = 540
        elif self.rect.centerx > 549:
            self.rect.centerx = 10

    def view_image(self):
        """
        Функция выбирает нужную картинку для персонажа в зависимости от направления движения
        и реализует движение ртом при движении
        :return: Присваивает переменной self.image нужное значение
        """
        if self.speedx == 0 and self.speedy == 0:
            self.image = pygame.transform.rotate(self.picture[1], self.an)
        else:
            if self.number_picture == 1:
                self.image = pygame.transform.rotate(self.picture[0], self.an)
                if self.time_image == 0:
                    self.number_picture = 2
                    self.time_image = 15
            else:
                self.image = pygame.transform.rotate(self.picture[1], self.an)
                if self.time_image == 0:
                    self.number_picture = 1
                    self.time_image = 15
            self.time_image -= 1


