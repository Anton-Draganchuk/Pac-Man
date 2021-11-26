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


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_pacman
        self.rect = self.image.get_rect()
        self.rect.center = 30, 650
        self.speedx = 0
        self.speedy = 0
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor(self.rect.centery / 20))

    def location(self):
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -2
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 2
        elif keystate[pygame.K_UP]:
            self.speedy = -2
        elif keystate[pygame.K_DOWN]:
            self.speedy = 2

        self.location()

        if self.speedy == -2 and number_map[self.up, self.number_x] == 1:
            self.speedy = 0
        if self.speedy == 2 and number_map[self.down, self.number_x] == 1:
            self.speedy = 0
        if self.speedx == -2 and number_map[self.number_y, self.left] == 1:
            self.speedx = 0
        if self.speedx == 2 and number_map[self.number_y, self.right] == 1:
            self.speedx = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy


# Создание рабочей поверхности
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Загрузка всех фото и аудио файлов
image_board = pygame.transform.scale(pygame.image.load('Board.png'), (560, 620))
image_pacman = pygame.transform.scale(pygame.image.load('Pacman.png'), (30, 30))

# Создание объектов классов
interface = Interface(screen)
pacman = Pacman()
all_sprites = pygame.sprite.Group()
all_sprites.add(pacman)

# Карта в виде массива
number_map = np.zeros((31, 28), dtype=np.int64)
font = pygame.font.Font(None, 20)
Screen2 = pygame.Surface((560, 620))
p = 1
for j in range(28):
    for i in range(31):
        for x in range(j*interface.square_size, (j + 1)*interface.square_size):
            for y in range(i*interface.square_size, (i + 1)*interface.square_size):
                if image_board.get_at((x, y)) != (0, 0, 0, 255):
                    p *= 0
        if p == 0:
            Screen2.blit(font.render('1', False, WHITE), (j*20 + 5, i*20 + 5))
            number_map[i, j] = 1
            p = 1
        else:
            Screen2.blit(font.render('0', False, WHITE), (j*20 + 5, i*20 + 5))
Screen2.set_colorkey(BLACK)


# Игровой цикл
finished = False

while not finished:
    clock.tick(FPS)
    # Прорисовка всех частей
    screen.fill(BLACK)
    interface.draw_board()
    interface.draw_grid()
    all_sprites.draw(screen)
    screen.blit(Screen2, (0, 60))

    # Обновление всех частей
    all_sprites.update()

    # Цикл событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    pygame.display.update()

pygame.quit()

