import pygame
from Data import *
import Level
import map_
import interface_
import ghost_
import pacman_

# Создание рабочей поверхности
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Файл с рекордом
score = open('Score.txt', 'r+')

# Загрузка всех фото и аудио файлов
image_board = pygame.transform.scale(pygame.image.load('Board.png'), (560, 620))

image_pacman = [pygame.transform.scale(pygame.image.load('Pacman/Pacman1.png'), (25, 25)),
                pygame.transform.scale(pygame.image.load('Pacman/Pacman2.png'), (25, 25))]

image_ghost_red = [pygame.transform.scale(pygame.image.load('Red Ghost/Left.png'), (40, 40)),
                   pygame.transform.scale(pygame.image.load('Red Ghost/Up.png'), (40, 40)),
                   pygame.transform.scale(pygame.image.load('Red Ghost/Right.png'), (40, 40)),
                   pygame.transform.scale(pygame.image.load('Red Ghost/Down.png'), (40, 40))]

image_ghost_pink = [pygame.transform.scale(pygame.image.load('Pink Ghost/Left.png'), (40, 40)),
                    pygame.transform.scale(pygame.image.load('Pink Ghost/Up.png'), (40, 40)),
                    pygame.transform.scale(pygame.image.load('Pink Ghost/Right.png'), (40, 40)),
                    pygame.transform.scale(pygame.image.load('Pink Ghost/Down.png'), (40, 40))]

image_ghost_blue = [pygame.transform.scale(pygame.image.load('Blue Ghost/Left.png'), (40, 40)),
                    pygame.transform.scale(pygame.image.load('Blue Ghost/Up.png'), (40, 40)),
                    pygame.transform.scale(pygame.image.load('Blue Ghost/Right.png'), (40, 40)),
                    pygame.transform.scale(pygame.image.load('Blue Ghost/Down.png'), (40, 40))]

Fruit = [pygame.transform.scale(pygame.image.load('Fruit/Cherry.png'), (20, 20)),
         pygame.transform.scale(pygame.image.load('Fruit/Strawberry.png'), (20, 20)),
         pygame.transform.scale(pygame.image.load('Fruit/Apple.png'), (20, 20)),
         pygame.transform.scale(pygame.image.load('Fruit/Peach.png'), (20, 20))]

# Список всех спрайтов
all_sprites = pygame.sprite.Group()

# Создание оюъектов классов
pacman = pacman_.Pacman(image_pacman)
interface = interface_.Interface(screen, image_board)
card = map_.Map(screen, image_board)
award = map_.Award(screen)
ghost_red = ghost_.GhostRed(image_ghost_red)
ghost_pink = ghost_.GhostPink(image_ghost_pink)
ghost_blue = ghost_.GhostBlue(image_ghost_blue)
all_sprites.add(pacman)
all_sprites.add(ghost_red)
all_sprites.add(ghost_pink)
all_sprites.add(ghost_blue)

# Превращение карты в массив
card.walls(interface, pacman)

# Запуск основного цикла игры
Level.circle(screen, clock, all_sprites, interface, card, score, Fruit, pacman, award)

# Закрытие файла и выход из игры
score.close()
pygame.quit()
