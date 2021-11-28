import pygame
from pathlib import Path

pygame.init()

small_dot_size = 10
small_dot_score = 10
big_dot_size = 40
big_dot_score = 50


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        """
        Конструктор класса спрайтов
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(0, 0))


class PacMan:
    def __init__(self, screen: pygame.Surface, size: int, x_starting, y_starting, wall_sprite):
        """
        Конструктор класса персонажей PacMan

        :param screen: экран рисования
        :param size: размер (диаметр)
        :param x_starting: начальная координата центра по горизонтали
        :param y_starting: начальная координата центра по вертикали
        :param wall_sprite: спрайт стен лабиринта
        :param size: размер (диаметр)
        """
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.size = size
        self.default_speed = 50
        self.wall_sprite = wall_sprite
        self.x = x_starting
        self.y = y_starting
        self.orientation = 'Up'
        self.vx = 0
        self.vy = 0
        self.image = pygame.transform.scale(pygame.image.load(Path('pacman.png').resolve()), (self.size, self.size))
        self.orientated_image = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.sprite = Sprite()

    def blit(self):
        """
        Рисует Пакмана на экране
        """
        self.get_coords()
        self.orientate_image()
        self.config_sprite()

    def orientate_image(self):
        """
        Поворачивает изображение Пакмана в соответствии с заданной его ориентацией в пространстве
        """
        if self.orientation == 'Up':
            self.orientated_image = pygame.transform.rotate(self.image, 90)
        elif self.orientation == 'Down':
            self.orientated_image = pygame.transform.rotate(self.image, 270)
        elif self.orientation == 'Left':
            self.orientated_image = pygame.transform.rotate(self.image, 180)
        else:
            self.orientated_image = pygame.transform.rotate(self.image, 0)

    def config_sprite(self):
        """
        Определяет спрайт Пакмана
        """
        self.sprite.image = self.orientated_image
        self.sprite.rect = self.sprite.image.get_rect(center=(self.x, self.y))

    def get_coords(self):
        """
        Определяет координаты Пакмана на экране
        """
        self.get_speed()
        x = self.x + self.vx * time
        y = self.y + self.vy * time
        if not self.check_collision(x, y):
            self.x = x
            self.y = y
        self.x = self.x % self.screen_width
        self.y = self.y % self.screen_height

    def get_speed(self):
        """
        Определяет скорость Пакмана
        """
        self.speed = self.default_speed

    def check_collision(self, x, y):
        """
        Проверяет столкновение Пакмана с координатами x, y со стенкой
        :return: True, если есть столкновение, иначе False
        """
        sprite = self.sprite
        sprite.rect = sprite.image.get_rect(center=(x, y))
        return pygame.sprite.collide_mask(sprite, self.wall_sprite)

    def check_eating(self, sprite: pygame.sprite.Sprite):
        """
        Проверяет, съедает ли Пакман объект с данным спрайтом
        """
        return pygame.sprite.collide_mask(self.sprite, sprite)

    def start_moving_left(self):
        self.vx = - self.speed
        self.vy = 0
        self.orientation = 'Left'

    def start_moving_right(self):
        self.vx = self.speed
        self.vy = 0
        self.orientation = 'Right'

    def start_moving_up(self):
        self.vx = 0
        self.vy = - self.speed
        self.orientation = 'Up'

    def start_moving_down(self):
        self.vx = 0
        self.vy = + self.speed
        self.orientation = 'Down'


class Dot:
    def __init__(self, screen: pygame.Surface, x, y, size, score_for_eating):
        """
        Конструктор класса точек

        :param screen: экран рисования
        :param x: координата центра по горизонтали
        :param y: координата центра по вертикали
        :param size: размер (диаметр)
        :param score_for_eating: количество очков за съедение точки
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.sprite = Sprite()
        self.score_for_eating = score_for_eating


class SmallDot(Dot):
    def __init__(self, screen: pygame.Surface, x, y):
        """
        Конструктор класса маленьких точек

        :param screen: экран рисования
        :param x: координата центра по горизонтали
        :param y: координата центра по вертикали
        """
        Dot.__init__(self, screen, x, y, size=small_dot_size, score_for_eating=small_dot_score)


class BigDot(Dot):
    def __init__(self, screen: pygame.Surface, x, y):
        """
        Конструктор класса больших точек

        :param screen: экран рисования
        :param x: координата центра по горизонтали
        :param y: координата центра по вертикали
        """
        Dot.__init__(self, screen, x, y, size=big_dot_size, score_for_eating=big_dot_score)


class Score:
    def __init__(self):
        """
        Конструктор класса счётчиков очков
        """
        self.score = 0

    def add(self, value):
        """
        Добавляет очки

        :param value: количество очков
        """
        self.score += value
