from Data import *
import pygame


class Interface:
    def __init__(self, screen, image):
        """
        Инициализация объекта
        :param screen: Основной экран
        :param image: Картинка карты
        """
        self.screen = screen
        self.board_x = 0
        self.board_y = 60
        self.square_size = int(WIDTH / 28)
        self.font = pygame.font.Font(None, 30)
        self.factor_time = 20
        self.image = image

    def draw_board(self):
        """
        Отрисовка игровой доски
        :return: Игровая доска
        """
        self.screen.blit(self.image, (self.board_x, self.board_y))

    def draw_highscore(self, score, award):
        """
        Функция отображение рекорда
        :param score: Файл с рекордом
        :param award: Объект одноименного класса, отвечающий за считывания очков
        :return: Выводит рекорд и записывает новый
        """
        self.screen.blit(self.font.render('High score', False, YELLOW), (400, 5))
        if int(score.read()) < award.score:
            score.seek(0)
            score.write(str(award.score))
        score.seek(0)
        self.screen.blit(self.font.render(score.read(), False, WHITE), (410, 30))
        score.seek(0)

    def draw_score(self, award):
        """
        Функция отображения количества очков
        :param award: Объект одноименного класса, отвечающий за считывание очков
        :return: Выводит колличество очков
        """
        self.screen.blit(self.font.render('Score', False, YELLOW), (255, 5))
        self.screen.blit(self.font.render(str(award.score), False, WHITE), (265, 30))

    def draw_factor(self, award):
        """
        Функция отображения множителя очков, срабатывает при съедание фруктов
        :param award: Объект одноименного класса
        :return: Выводит на экран множитель
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
