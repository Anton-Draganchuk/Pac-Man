import pygame
import numpy as np

FPS = 60

# Цвета
GREEN = [0, 255, 0]
BLACK = [0, 0, 0]
WHITE = (255, 255, 255)

# Размеры экрана
WIDTH = 560
HEIGHT = 720


class Interface:
    def __init__(self, screen):
        self.screen = screen
        self.board_x = 0
        self.board_y = 60
        self.square_size = int(WIDTH / 28)
        self.font = pygame.font.Font(None, 20)

    def draw_board(self):
        """
        Отрисовка игровой доски
        :return: Игровая доска
        """
        self.screen.blit(image_board, (self.board_x, self.board_y))

    def draw_grid(self):
        """
        Отрисовка решетки для наглядного видения поля
        :return: Игровая решетка
        """
        self.Surface = pygame.Surface((WIDTH, HEIGHT))
        x = 0
        while x != WIDTH:
            pygame.draw.line(self.Surface, GREEN, (x, 0), (x, HEIGHT), 2)
            x += self.square_size
        y = 0
        while y != HEIGHT:
            pygame.draw.line(self.Surface, GREEN, (0, y), (WIDTH, y), 2)
            y += self.square_size

        self.Surface.set_alpha(60)
        self.screen.blit(self.Surface, (0, 0))

    def draw_operating_values(self):
        self.screen.blit(self.font.render('x = ' + str(pacman.rect.centerx) +
                                          '  y = ' + str(pacman.rect.centery), False, WHITE), (100, 5))

    def draw_score(self):
        award.sum_score()
        self.screen.blit(self.font.render(str(award.score), False, WHITE), (5, 5))


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.an = 0
        self.image = pygame.transform.rotate(image_pacman1, self.an)
        self.rect = self.image.get_rect()
        self.rect.center = 30, 650
        self.speedx = 0
        self.speedy = 0
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor(self.rect.centery / 20))
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
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))

    def update(self):
        # Получаем значения вокруг пакмена, с 4 сторон
        self.location()

        # Поворот с режимом залипания клавиши на колличество ходов time2_turn
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or self.flag_left > 0:
            if map.number_map[self.number_y, self.left] != 1 and self.rect.centery % 20 == 10:
                self.speedx = -2
                self.an = 90
                self.speedy = 0
                self.flag_left = 0
            elif self.flag_left == 0:
                self.flag_left = self.time2_turn
            else:
                self.flag_left -= 1

        elif keystate[pygame.K_RIGHT] or self.flag_right > 0:
            if map.number_map[self.number_y, self.right] != 1 and self.rect.centery % 20 == 10:
                self.speedx = 2
                self.an = -90
                self.speedy = 0
                self.flag_right = 0
            elif self.flag_right == 0:
                self.flag_right = self.time2_turn
            else:
                self.flag_right -= 1

        elif keystate[pygame.K_UP] or self.flag_up > 0:
            if map.number_map[self.up, self.number_x] != 1 and self.rect.centerx % 20 == 10:
                self.speedy = -2
                self.an = 0
                self.speedx = 0
                self.flag_up = 0
            elif self.flag_up == 0:
                self.flag_up = self.time2_turn
            else:
                self.flag_up -= 1

        elif keystate[pygame.K_DOWN] or self.flag_down > 0:
            if map.number_map[self.down, self.number_x] != 1 and self.rect.centerx % 20 == 10:
                self.speedy = 2
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
        if self.speedy == -2 and map.number_map[self.up, self.number_x] == 1:
            self.speedy = 0
        if self.speedy == 2 and map.number_map[self.down, self.number_x] == 1:
            self.speedy = 0
        if self.speedx == -2 and map.number_map[self.number_y, self.left] == 1:
            self.speedx = 0
        if self.speedx == 2 and map.number_map[self.number_y, self.right] == 1:
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
        if self.speedx == 0 and self.speedy == 0:
            self.image = pygame.transform.rotate(image_pacman1, self.an)
        else:
            if self.number_picture == 1:
                self.image = pygame.transform.rotate(image_pacman1, self.an)
                if self.time_image == 0:
                    self.number_picture = 2
                    self.time_image = 15
            else:
                self.image = pygame.transform.rotate(image_pacman2, self.an)
                if self.time_image == 0:
                    self.number_picture = 1
                    self.time_image = 15
            self.time_image -= 1


class Map:
    def __init__(self, screen):
        self.number_map = np.zeros((31, 28), dtype=np.int64)
        self.font = pygame.font.Font(None, 20)
        self.Screen2 = pygame.Surface((560, 620))
        self.screen = screen

    def walls(self):
        p = 1
        for j in range(28):
            for i in range(31):
                for x in range(j*interface.square_size, (j + 1)*interface.square_size):
                    for y in range(i*interface.square_size, (i + 1)*interface.square_size):
                        if image_board.get_at((x, y)) != (0, 0, 0, 255):
                            p *= 0
                if p == 0:
                    self.number_map[i, j] = 1
                    p = 1

    def update(self):
        self.number_map[pacman.number_y, pacman.number_x] = 2

    def draw(self):
        self.Screen2.fill(BLACK)
        for j in range(28):
            for i in range(31):
                self.Screen2.blit(self.font.render(str(self.number_map[i, j]), False, WHITE), (j*20 + 5, i*20 + 5))
        self.Screen2.set_colorkey(BLACK)
        self.screen.blit(self.Screen2, (0, 60))

    def reset(self):
        self.number_map[pacman.number_y, pacman.number_x] = 3


class Award:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.screen2 = pygame.Surface((560, 620))

    def draw(self):
        self.screen2.fill(BLACK)
        for j in range(28):
            for i in range(31):
                if map.number_map[i, j] == 0:
                    pygame.draw.circle(self.screen2, WHITE, (j*20 + 10, i*20 + 10), 3)
        self.screen2.set_colorkey(BLACK)
        self.screen.blit(self.screen2, (0, 60))

    def sum_score(self):
        self.score = 0
        for j in range(28):
            for i in range(31):
                if map.number_map[i, j] == 3:
                    self.score += 1


# Создание рабочей поверхности
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Загрузка всех фото и аудио файлов
image_board = pygame.transform.scale(pygame.image.load('Board.png'), (560, 620))
image_pacman = pygame.transform.scale(pygame.image.load('Pacman.png'), (30, 30))
image_pacman1 = pygame.transform.scale(pygame.image.load('Pacman1.png'), (30, 30))
image_pacman2 = pygame.transform.scale(pygame.image.load('Pacman2.png'), (30, 30))

# Создание объектов классов
interface = Interface(screen)
pacman = Pacman()
map = Map(screen)
award = Award(screen)
all_sprites = pygame.sprite.Group()
all_sprites.add(pacman)

# Карта в виде массива
map.walls()

# Игровой цикл
finished = False

while not finished:
    clock.tick(FPS)
    # Обновление всех частей
    all_sprites.update()
    map.update()

    # Прорисовка всех частей
    screen.fill(BLACK)
    interface.draw_board()
    # interface.draw_grid()
    all_sprites.draw(screen)
    award.draw()
    # map.draw()
    interface.draw_score()
    interface.draw_operating_values()

    # Цикл событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    # Восстановление массива с картой
    map.reset()

    pygame.display.update()

pygame.quit()

