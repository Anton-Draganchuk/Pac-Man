from Data import *
import pygame
from final_screen import end_screen_loop


def circle(screen, clock, all_sprites, interface, map, score, fruit, pacman, award):
    """
    Функция игрового цикла, в котором происходит обновление всех элементов и их прорисовка
    :param screen: Основной экран на котором все рисуется
    :param clock: Время для отсчитывания кадров в секунду
    :param all_sprites: Список из всех спрайтов
    :param interface: Объект одноименного класса, отвечает за стационарные детали на экране
    :param map: Объект одноименного класса, отвечает за карту в виде массива
    :param score: Файл в котором записан рекордное колличество очков
    :param fruit: Список из всех картинок фруктов
    :param pacman: Объект одноименного класса, оьвечает за основного персонажа
    :param award: Объект одноименного класса, отвечает за расстановку фруктов и очков
    :return: Игровой экран с возможностью регировать на нажатие клавиш
    """
    # Пауза в игре
    pause = 0

    # Игровой цикл
    finished = False

    while not finished:
        clock.tick(FPS)

        if not pause:
            # Обновление всех частей
            all_sprites.update(pacman, map, award)

            # Прорисовка всех частей
            screen.fill(BLACK)
            interface.draw_board()
            award.draw_dot(map)
            award.draw_fruit(map, fruit)
            award.update(map, pacman)
            interface.draw_factor(award)
            all_sprites.draw(screen)
            interface.draw_score(award)
            interface.draw_highscore(score, award)

            # Определяем необходимость завершить игру и показать финальный экран
            finished = end_screen_loop(screen, award, pacman, all_sprites)

        # Цикл событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                finished = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if pause == 0:
                    pause = 1
                else:
                    pause = 0

        pygame.display.update()
