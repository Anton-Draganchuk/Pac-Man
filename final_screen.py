from Data import *
import pygame


def end_game(pacman: pygame.sprite.Sprite, all_sprites: pygame.sprite.Group):
    """
    Функция проверяет столкновение Пакмена с призраками
    :param pacman: спрайт Пакмена
    :param all_sprites: группа всех спрайтов
    :return: True, если столкновение произошло, иначе False
    """
    for sprite in all_sprites:
        if sprite is not pacman:
            if pygame.sprite.collide_mask(pacman, sprite):
                return True
    return False


def show_end_screen(screen, award):
    """
    Выводит финальный экран с набранными очками
    :param screen: основной экран на котором все рисуется
    :param award: объект одноименного класса, отвечает за расстановку фруктов и очков
    """
    scr = pygame.image.load('final.png')
    final = pygame.transform.scale(scr, (WIDTH, HEIGHT))
    screen.blit(final, (0, 0))
    text = pygame.font.Font(None, 60).render(f'Your score is {award.score}!', False, WHITE)
    screen.blit(text, (100, 530))
    text = pygame.font.Font(None, 60).render(f'Press Esc to exit.', False, WHITE)
    screen.blit(text, (115, 620))


def end_screen_loop(screen, award, pacman, all_sprites):
    """
    Функция отрисовывает финальный экран до тех пор, пока не произведён выход из игры
    :param screen: основной экран на котором все рисуется
    :param award: объект одноименного класса, отвечает за расстановку фруктов и очков
    :param pacman: спрайт Пакмена
    :param all_sprites: группа всех спрайтов
    :return: True, если произведён выход из игры, иначе False
    """
    finished = False
    if end_game(pacman, all_sprites):
        clock = pygame.time.Clock()
        while not finished:
            show_end_screen(screen, award)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    finished = True
            clock.tick(FPS)
    return finished
