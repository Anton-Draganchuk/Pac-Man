import pygame
import numpy as np

FPS = 60

# Цвета
GREEN = [0, 255, 0]
BLACK = [0, 0, 0]
WHITE = (255, 255, 255)
PINK = [236, 136, 125]

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
        self.screen.blit(self.font.render(str(award.score), False, WHITE), (5, 5))


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.an = 0
        self.image = pygame.transform.rotate(image_pacman2, self.an)
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
        # Поворот налево
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a] or self.flag_left > 0:
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
        elif keystate[pygame.K_RIGHT] or keystate[pygame.K_d] or self.flag_right > 0:
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
        elif keystate[pygame.K_UP] or keystate[pygame.K_w] or self.flag_up > 0:
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
        elif keystate[pygame.K_DOWN] or keystate[pygame.K_s] or self.flag_down > 0:
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
        if self.speedx == 0 and self.speedy == 0:
            self.image = pygame.transform.rotate(image_pacman2, self.an)
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
                        if image_board.get_at((x, y)) != (0, 0, 0, 0):
                            p *= 0
                if p == 0:
                    self.number_map[i, j] = 1
                    p = 1
                elif 7 <= j <= 20 and 9 <= i <= 19:
                    self.number_map[i, j] = 3
                elif i == 14 and (0 <= j <= 5 or 22 <= j <= 27):
                    self.number_map[i, j] = 3
        self.number_map[pacman.number_y, pacman.number_x] = 3
        self.number_map[pacman.number_y, pacman.number_x - 1] = 3

    def update(self):
        if self.number_map[pacman.number_y, pacman.number_x] == 0:
            award.score += 10
        elif self.number_map[pacman.number_y, pacman.number_x] == 4:
            award.score += 40
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

    def draw_dot(self):
        self.screen2.fill(BLACK)
        for j in range(28):
            for i in range(31):
                if map.number_map[i, j] == 0:
                    pygame.draw.rect(self.screen2, PINK, [j*20 + 7, i*20 + 7, 6, 6])

    def set_fruit(self):
        global Fruit
        i, j = 0, 0
        for k in range(len(Fruit)):
            while map.number_map[i, j] != 0:
                i, j = np.random.randint(0, 30), np.random.randint(0, 27)
            map.number_map[i, j] = 4

    def draw_fruit(self):
        p = 0
        for j in range(28):
            for i in range(31):
                if p < 4 and map.number_map[i, j] == 4:
                    self.screen2.blit(Fruit[p], (j*20, i*20))
                    p += 1
        self.screen2.set_colorkey(BLACK)
        self.screen.blit(self.screen2, (0, 60))


class Introduction:
    def __init__(self, screen):
        self.screen = screen


class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_ghost
        self.rect = self.image.get_rect()
        self.rect.center = 280, 410
        self.speedx = -1
        self.speedy = 0
        self.speed = 1
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
        self.distance = []

    def location(self):
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))

    def distance2_pacman(self):
        self.dist_left = np.sqrt((self.left - pacman.number_x)**2 + (self.number_y - pacman.number_y)**2)
        self.dist_right = np.sqrt((self.right - pacman.number_x)**2 + (self.number_y - pacman.number_y)**2)
        self.dist_up = np.sqrt((self.number_x - pacman.number_x)**2 + (self.up - pacman.number_y)**2)
        self.dist_down = np.sqrt((self.number_x - pacman.number_x)**2 + (self.down - pacman.number_y)**2)
        self.distance = [self.dist_left, self.dist_right, self.dist_up, self.dist_down]

    def update(self):
        # Получаем значения вокруг призрака, с 4 сторон
        self.location()
        self.distance2_pacman()

        # Перемещение призрака
        if self.rect.centerx % 20 == 10 and self.rect.centery % 20 == 10:
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

            if self.dist_up <= min(self.distance) and\
                    self.speedy <= 0 and map.number_map[self.up, self.number_x] != 1:
                self.speedy = - self.speed
                self.speedx = 0
            elif self.dist_down <= min(self.distance) and\
                    self.speedy >= 0 and map.number_map[self.down, self.number_x] != 1:
                self.speedy = self.speed
                self.speedx = 0
            elif self.dist_left <= min(self.distance) and\
                    self.speedx <= 0 and map.number_map[self.number_y, self.left] != 1:
                self.speedy = 0
                self.speedx = - self.speed
            elif self.dist_right <= min(self.distance) and\
                    self.speedx >= 0 and map.number_map[self.number_y, self.right] != 1:
                self.speedy = 0
                self.speedx = self.speed

        # Перемещение на значение его скорости
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Прохождение через тунель
        if self.rect.centerx < 9:
            self.rect.centerx = 540
        elif self.rect.centerx > 549:
            self.rect.centerx = 10

        if self.number_x == pacman.number_x and self.number_y == pacman.number_y:
            all_sprites.remove(pacman)


# Создание рабочей поверхности
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Загрузка всех фото и аудио файлов
image_board = pygame.transform.scale(pygame.image.load('Board.png'), (560, 620))
image_pacman1 = pygame.transform.scale(pygame.image.load('Pacman1.png'), (25, 25))
image_pacman2 = pygame.transform.scale(pygame.image.load('Pacman2.png'), (25, 25))
image_ghost = pygame.transform.scale(pygame.image.load('Ghost.png'), (25, 25))
image_cherry = pygame.transform.scale(pygame.image.load('Cherry.png'), (20, 20))
image_strawberry = pygame.transform.scale(pygame.image.load('Strawberry.png'), (20, 20))
image_apple = pygame.transform.scale(pygame.image.load('Apple.png'), (20, 20))
image_peach = pygame.transform.scale(pygame.image.load('Peach.png'), (20, 20))
Fruit = [image_cherry, image_peach, image_apple, image_strawberry]

# Создание объектов классов
interface = Interface(screen)
pacman = Pacman()
ghost = Ghost()
map = Map(screen)
award = Award(screen)
all_sprites = pygame.sprite.Group()
all_sprites.add(pacman)
all_sprites.add(ghost)

# Карта в виде массива
map.walls()
award.set_fruit()

# Режим разработчика
developer_mode = 0

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
    if developer_mode:
        interface.draw_grid()
    award.draw_dot()
    award.draw_fruit()
    if developer_mode:
        map.draw()
    all_sprites.draw(screen)
    interface.draw_score()
    interface.draw_operating_values()

    # Цикл событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if developer_mode == 0:
                developer_mode = 1
            else:
                developer_mode = 0

    # Восстановление массива с картой
    map.reset()

    pygame.display.update()

pygame.quit()

