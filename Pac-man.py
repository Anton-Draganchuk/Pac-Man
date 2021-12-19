import pygame
import numpy as np

FPS = 60

# Цвета
GREEN = [0, 255, 0]
BLACK = [0, 0, 0]
WHITE = (255, 255, 255)
PINK = [236, 136, 125]
YELLOW = [255, 255, 0]

# Размеры экрана
WIDTH = 560
HEIGHT = 720


class Interface:
    def __init__(self, interface_screen):
        """
        Класс игрового окна
        :param interface_screen: экран рисования окна
        """
        self.screen = interface_screen
        self.board_x = 0
        self.board_y = 60
        self.square_size = int(WIDTH / 28)
        self.font = pygame.font.Font(None, 30)
        self.factor_time = 20
        self.level = 1

    def draw_board(self):
        """
        Отрисовка игровой доски
        """
        self.screen.blit(image_board, (self.board_x, self.board_y))

    def draw_grid(self):
        """
        Отрисовка решетки для наглядного видения поля
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
        self.screen.blit(self.font.render('None', False, WHITE), (20, 5))

    def draw_highscore(self):
        """
        Выводит текст "High score" и значение рекорда на экран
        """
        global score
        self.screen.blit(self.font.render('High score', False, YELLOW), (400, 5))
        if int(score.read()) < award.score:
            score.seek(0)
            score.write(str(award.score))
        score.seek(0)
        self.screen.blit(self.font.render(score.read(), False, WHITE), (410, 30))
        score.seek(0)

    def draw_score(self):
        """
        Выводит текст "Score" и количество очков на экран
        """
        self.screen.blit(self.font.render('Score', False, YELLOW), (255, 5))
        self.screen.blit(self.font.render(str(award.score), False, WHITE), (265, 30))

    def draw_health(self):
        """
        Выводит текст "Health" и здоровье Пакмена на экран
        """
        self.screen.blit(self.font.render('Health', False, YELLOW), (130, 5))
        self.screen.blit(self.font.render(str(pacman.health), False, WHITE), (140, 30))

    def draw_level(self):
        """
        Выводит текст "Level" и уровень на экран
        """
        self.screen.blit(self.font.render('Level', False, YELLOW), (15, 5))
        self.screen.blit(self.font.render(str(self.level), False, WHITE), (25, 30))

    def draw_factor(self):
        """
        Выводит надпись "X10" на экран, при необходимости осуществляет её мигание
        """
        if award.fruit_time > 120:
            self.screen.blit(pygame.font.Font(None, 40).render('X 10', False, YELLOW), (255, 400))
        elif award.fruit_time > 0:
            if self.factor_time == 0:
                self.factor_time = 20
            elif self.factor_time < 10:
                self.screen.blit(pygame.font.Font(None, 40).render('X 10', False, YELLOW), (255, 400))
                self.factor_time -= 1
            else:
                self.factor_time -= 1

    def new_level(self):
        """
        Осуществляет переход на новый уровень при отсутствии точек на экране
        """
        if (map.number_map == 0).sum() + (map.number_map == 4).sum() <= 56:
            interface.level += 1
            pacman.get_started()
            ghost_red.get_started()
            map.__init__(screen)
            map.walls()


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        """
        Класс Пакмена
        """
        pygame.sprite.Sprite.__init__(self)
        self.an = 0
        self.image = pygame.transform.rotate(image_pacman[1], self.an)
        self.rect = self.image.get_rect()
        self.time2_turn = 20
        self.number_picture = 1
        self.time_image = 15
        self.health = 3

        self.get_started()

    def get_started(self):
        """
        Помещает Пакмена в начальное положение
        """
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

    def location(self):
        """
        Получает значение координат Пакмена и границ его спрайта (для определения столкновения с препятствиями)
        :return:
        """
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))

    def update(self):
        """
        Осуществляет движение Пакмена и обновляет его спрайт
        """
        # Получаем значения вокруг пакмена, с 4 сторон
        self.location()

        # Поворот с режимом залипания клавиши на колличество ходов time2_turn
        keystate = pygame.key.get_pressed()
        # Поворот налево
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
        """
        Определяет, какое изображение Пакмена должно показываться на данный момент, осуществляет анимацию Пакмена
        """
        if self.speedx == 0 and self.speedy == 0:
            self.image = pygame.transform.rotate(image_pacman[1], self.an)
        else:
            if self.number_picture == 1:
                self.image = pygame.transform.rotate(image_pacman[0], self.an)
                if self.time_image == 0:
                    self.number_picture = 2
                    self.time_image = 15
            else:
                self.image = pygame.transform.rotate(image_pacman[1], self.an)
                if self.time_image == 0:
                    self.number_picture = 1
                    self.time_image = 15
            self.time_image -= 1

    def hit(self):
        """
        Уменьшает количество жизней Пакмена, возвращает его в начальное положение
        """
        global game_over
        self.health -= 1
        if self.health <= 0:
            self.health = 0
            game_over = True
            all_sprites.remove(pacman)
        else:
            self.get_started()


class Map:
    def __init__(self, map_screen):
        """
        Класс игровой карты
        :param map_screen: экран рисования карты
        """
        self.number_map = np.zeros((33, 28), dtype=np.int64)
        self.font = pygame.font.Font(None, 20)
        self.Screen2 = pygame.Surface((560, 660))
        self.screen = map_screen

    def walls(self):
        """
        Определяет расположение стен и начального положения Пакмена на карте
        """
        p = 1
        for j in range(28):
            for i in range(31):
                for x in range(j * interface.square_size, (j + 1) * interface.square_size):
                    for y in range(i * interface.square_size, (i + 1) * interface.square_size):
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

    def draw(self):
        """
        Выводит на экран значения параметра number_map в каждой точке карты (для режима разработчика)
        """
        self.Screen2.fill(BLACK)
        for j in range(28):
            for i in range(33):
                self.Screen2.blit(self.font.render(str(self.number_map[i, j]), False, WHITE), (j * 20 + 5, i * 20 + 5))
        self.Screen2.set_colorkey(BLACK)
        self.screen.blit(self.Screen2, (0, 60))


class Award:
    def __init__(self, award_screen):
        """
        Класс менеджера рисования целей (точек и фруктов)
        :param award_screen: экран рисования точек и фруктов
        """
        self.screen = award_screen
        self.score = 0
        self.screen2 = pygame.Surface((560, 660))
        self.time = 600
        self.fruit = 0
        self.fruit_time = 0
        self.factor = 1

    def draw_dot(self):
        """
        Рисует точки на экране
        """
        self.screen2.fill(BLACK)
        for j in range(28):
            for i in range(31):
                if map.number_map[i, j] == 0:
                    pygame.draw.rect(self.screen2, PINK, [j * 20 + 7, i * 20 + 7, 6, 6])

    def set_fruit(self):
        """
        Добавляет фрукт на карту в случайном месте, если других фруктов нет
        """
        i, j = 0, 0
        if self.time == 0 and (map.number_map == 4).sum() == 0:
            while map.number_map[i, j] != 0 and self.fruit < 3:
                i = np.random.randint(0, 31)
                j = np.random.randint(0, 28)
            map.number_map[i, j] = 4
            self.fruit += 1
        else:
            self.time -= 1

    def update(self):
        """
        Осуществляет съедение точек и фруктов, увеличивает количество очков
        """
        if map.number_map[pacman.number_y, pacman.number_x] == 0:
            self.score += 10 * self.factor
        elif map.number_map[pacman.number_y, pacman.number_x] == 4:
            self.fruit_time = 300
            self.time = np.random.randint(800, 1200)
        map.number_map[pacman.number_y, pacman.number_x] = 3

        if self.fruit_time != 0:
            self.factor = 10
            self.fruit_time -= 1
        else:
            self.factor = 1

    def draw_fruit(self):
        """
        Добавляет фрукт на карту при необходимости, рисует все фрукты на экране
        """
        self.set_fruit()

        for j in range(28):
            for i in range(31):
                if self.fruit < 4 and map.number_map[i, j] == 4:
                    self.screen2.blit(Fruit[self.fruit - 1], (j * 20, i * 20))

        if (map.number_map == 4).sum() == 0:
            for f in range(self.fruit):
                self.screen2.blit(pygame.transform.scale(Fruit[f],
                                                         (40, 40)), ((28 - 2*self.fruit + 2*f) * 20, 31 * 20))
        else:
            for f in range(self.fruit - 1):
                self.screen2.blit(pygame.transform.scale(Fruit[f],
                                                         (40, 40)), ((28 - 2*self.fruit + 2 + 2*f) * 20, 31 * 20))

        self.screen2.set_colorkey(BLACK)
        self.screen.blit(self.screen2, (0, 60))


class Introduction:
    def __init__(self, screen):
        self.screen = screen


class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        """
        Класс призраков
        """
        pygame.sprite.Sprite.__init__(self)
        self.get_started()
        self.speedx = -self.speed
        self.speedy = 0
        self.dist_left = 0
        self.dist_right = 0
        self.dist_up = 0
        self.dist_down = 0
        self.mode = 1
        self.time = 0
        self.distance = []
        self.x = 0
        self.y = 0

    def get_started(self):
        """
        Помещает призрака в начальное положение
        """
        self.speed = self.get_speed()
        self.number_x = 0
        self.number_y = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

    def get_speed(self):
        """
        Определяет скорость призрака в зависимости от уровня
        :return: скорость призрака
        """
        return 1

    def distance2_pacman(self, x, y):
        """
        Определяет расстояние от призрака до Пакмена и до краёв карты
        :param x: координата Пакмена по горизонтали
        :param y: координата Пакмена по вертикали
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

    def get_direction(self):
        """
        Определяет направление движения в зависимости от расстояния до Пакмена и краёв карты;
        Устанавливает соответствующее значение скорости призрака по вертикали и горизонтали
        """
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

    def get_distance(self):
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

    def set_mode(self):
        """
        Определяет режим движения призрака в зависимости от времени
        Увеличивает значение параметра времени на 1
        """
        if self.time <= 560:
            self.mode = 2
        elif self.time <= 1520:
            self.mode = 1
        else:
            self.time = 0
        self.time += 1

    def update(self):
        """
        Обновленяет спрайт призрака
        """
        # Установить режим с помощью таймера time
        self.set_mode()

        # Перемещение призрака
        if self.rect.centerx % 20 == 10 and self.rect.centery % 20 == 10:
            if self.mode == 1:
                self.mode1()
            elif self.mode == 2:
                self.mode2()

        # Перемещение на значение его скорости
        self.x += self.speedx
        self.y += self.speedy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Прохождение через тунель
        if self.rect.centerx < 9:
            self.rect.centerx = 540
            self.x = 540
        elif self.rect.centerx > 549:
            self.rect.centerx = 10
            self.x = 10

        # Выбор картинки по направлению
        self.get_image()

        if self.number_x == pacman.number_x and self.number_y == pacman.number_y:
            pacman.hit()

    def get_image(self):
        pass

    def mode1(self):
        pass

    def mode2(self):
        pass


class GhostRed(Ghost):
    def __init__(self):
        """
        Класс красных призраков
        """
        super(GhostRed, self).__init__()
        self.image = image_ghost_red[0]
        self.rect = self.image.get_rect()
        self.rect.center = 280, 410
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.number_x = int(np.floor(self.rect.centerx / 20))
        self.number_y = int(np.floor((self.rect.centery - 60) / 20))
        self.up = int(np.floor((self.rect.centery - 71) / 20))
        self.down = int(np.floor((self.rect.centery - 49) / 20))
        self.left = int(np.floor((self.rect.centerx - 11) / 20))
        self.right = int(np.floor((self.rect.centerx + 11) / 20))

    def get_image(self):
        """
        Устанавливает изображение в зависимости от направления движения призрака
        """
        if self.speedx < 0:
            self.image = image_ghost_red[0]
        elif self.speedx > 0:
            self.image = image_ghost_red[2]
        elif self.speedy > 0:
            self.image = image_ghost_red[3]
        elif self.speedy < 0:
            self.image = image_ghost_red[1]

    def mode1(self):
        """
        Осуществляет движение призрака в первом режиме (преследование)
        """
        # Получаем значения вокруг призрака, с 4 сторон
        self.distance2_pacman(pacman.number_x, pacman.number_y)

        # Перемещение призрака
        self.get_distance()
        self.get_direction()

    def mode2(self):
        """
        Осуществляет движение призрака во втором режиме (движение к левому нижнему углу)
        """
        # Получаем значения вокруг призрака, с 4 сторон
        self.distance2_pacman(0, 35)

        # Перемещение призрака
        self.get_distance()
        self.get_direction()


def show_end_screen(end_screen):
    """
    Выводит экран окончания игры
    :param end_screen: экран рисования
    """
    end_screen.blit(game_over_screen, (0, 0))


# Создание рабочей поверхности
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Загрузка всех фото и аудио файлов
image_board = pygame.transform.scale(pygame.image.load('Board.png'), (560, 620))

image_pacman = [pygame.transform.scale(pygame.image.load('Pacman/Pacman1.png'), (25, 25)),
                pygame.transform.scale(pygame.image.load('Pacman/Pacman2.png'), (25, 25))]

image_ghost_red = [pygame.transform.scale(pygame.image.load('Red Ghost/Left.png'), (40, 40)),
                   pygame.transform.scale(pygame.image.load('Red Ghost/Up.png'), (40, 40)),
                   pygame.transform.scale(pygame.image.load('Red Ghost/Right.png'), (40, 40)),
                   pygame.transform.scale(pygame.image.load('Red Ghost/Down.png'), (40, 40))]

Fruit = [pygame.transform.scale(pygame.image.load('Fruit/Cherry.png'), (20, 20)),
         pygame.transform.scale(pygame.image.load('Fruit/Strawberry.png'), (20, 20)),
         pygame.transform.scale(pygame.image.load('Fruit/Apple.png'), (20, 20)),
         pygame.transform.scale(pygame.image.load('Fruit/Peach.png'), (20, 20))]

game_over_screen = pygame.transform.scale(pygame.image.load('GameOver.png'), (WIDTH, HEIGHT))

# Создание объектов классов
interface = Interface(screen)
pacman = Pacman()
ghost_red = GhostRed()
map = Map(screen)
award = Award(screen)
all_sprites = pygame.sprite.Group()
all_sprites.add(pacman)
all_sprites.add(ghost_red)

# Файл с рекордом
score = open('Score.txt', 'r+')

# Карта в виде массива
map.walls()

# Режим разработчика
developer_mode = 0

# Пауза в игре
pause = 0

# Игровой цикл
game_over = False
finished = False

while not finished and not game_over:
    clock.tick(FPS)
    print(ghost_red.speedx, ghost_red.speedy)

    if not pause:
        # Переход на следующий уровень
        interface.new_level()

        # Обновление всех частей
        all_sprites.update()

        # Прорисовка всех частей
        screen.fill(BLACK)
        interface.draw_board()
        if developer_mode:
            interface.draw_grid()
        award.draw_dot()
        award.draw_fruit()
        award.update()
        if developer_mode:
            map.draw()
            interface.draw_operating_values()
        interface.draw_factor()
        all_sprites.draw(screen)
        interface.draw_score()
        interface.draw_highscore()
        interface.draw_health()
        interface.draw_level()

    # Цикл событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            finished = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if developer_mode == 0:
                developer_mode = 1
            else:
                developer_mode = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if pause == 0:
                pause = 1
            else:
                pause = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            for j in range(28):
                for i in range(31):
                    if map.number_map[i, j] == 0:
                        map.number_map[i, j] = 3

    pygame.display.update()

# Вывод экрана окончания игры
while not finished and game_over:
    clock.tick(FPS)
    show_end_screen(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            finished = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if developer_mode == 0:
                developer_mode = 1
            else:
                developer_mode = 0

score.close()
pygame.quit()
