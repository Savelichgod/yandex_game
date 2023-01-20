import pygame
from time import sleep
"""Модуль игрового поля"""


class Board:
    """Класс доски"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.bot = True
        self.player = 'o'
        self.main_color = (0, 0, 0)
        self.sub_color = (255, 255, 255)
        self.score = {'x': 0, 'o': 0, '=': 0}

    def restart(self):
        """Перезапуск игры"""
        self.board = [[0] * self.width for _ in range(self.height)]

    def change_player(self):
        """Смена очередности хода"""
        if self.player == 'o':
            self.player = 'x'
        else:
            self.player = 'o'

    def set_view(self, left, top, cell_size):
        """Изменение масштабирования и отступов"""
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def show_game_result(self, winer, screen):
        sleep(2)
        self.score[winer] += 1
        game_over_font = pygame.font.SysFont('Arial', 85)
        screen.fill((0, 0, 0))
        if winer == '=':
            text = game_over_font.render(f"      НИЧЬЯ", True, (125, 55, 160))
        else:
            text = game_over_font.render(f"ПОБЕДИЛ: {winer.upper()}", True, (125, 55, 160))
        screen.blit(text, (25, 140))
        pygame.display.flip()
        sleep(2)
        self.restart()
        pygame.display.flip()

    def render(self, sur):
        """Отрисовка поля"""
        sur.fill(self.main_color)
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 'o':
                    radius = self.cell_size // 2
                    pygame.draw.circle(sur, (255, 0, 0), (
                        self.left + x * self.cell_size + radius, self.top + y * self.cell_size + radius), radius - 3, 3)
                if self.board[y][x] == 'x':
                    pygame.draw.line(sur, (0, 1, 255), (self.left + x * self.cell_size, self.top + y * self.cell_size),
                                     (self.left + x * self.cell_size + self.cell_size,
                                      self.top + y * self.cell_size + self.cell_size), 3)
                    pygame.draw.line(sur, (0, 1, 255),
                                     (self.left + x * self.cell_size, self.top + (y + 1) * self.cell_size),
                                     (self.left + x * self.cell_size + self.cell_size, self.top + y * self.cell_size),
                                     3)
                pygame.draw.rect(sur, self.sub_color, (
                    self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size), 2)
        font = pygame.font.SysFont('Arial', 40)
        text = font.render(f'Ход игрока: {self.player}', True, self.sub_color)
        text_1 = font.render(f'счёт x: {self.score["x"]} счёт o: {self.score["o"]}', True, (self.sub_color))
        sur.blit(text, (sur.get_size()[0] // 2 - text.get_size()[0] // 2, 0))
        sur.blit(text_1, (sur.get_size()[0] // 2 - text_1.get_size()[0] // 2, 350))
        pygame.display.flip()

    def is_game_over(self):
        """Проверка окончания игры"""
        lines = [[self.board[0][i] for i in range(3)], [self.board[1][i] for i in range(3)],
                 [self.board[2][i] for i in range(3)], [self.board[i][0] for i in range(3)],
                 [self.board[i][1] for i in range(3)], [self.board[i][2] for i in range(3)],
                 [self.board[i][i] for i in range(3)], [self.board[i][2 - i] for i in range(3)]]
        for line in lines:
            if (len(set(line)) == 1) and line[0] != 0:
                return line[0]
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        return '='

    def player_move(self, pos):
        """Ход игрока (пользователя)"""
        x, y = pos
        if (self.left <= x <= self.left + self.width * self.cell_size) and (
                self.top <= y <= self.top + self.height * self.cell_size):
            c = (x - self.left) // self.cell_size
            r = (y - self.top) // self.cell_size
            if self.board[r][c] == 0:
                self.board[r][c] = self.player
                self.change_player()

    def can_win_in_one_move(self, player):
        """Проверка можем ли победить за один ход"""
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 0:
                    self.board[y][x] = player
                    res = self.is_game_over()
                    self.board[y][x] = 0
                    if res:
                        return y, x
        return False

    def bot_move(self):
        """Ход бота"""
        if self.bot and self.player == 'o' and not self.is_game_over():
            if self.can_win_in_one_move('o'):
                y, x = self.can_win_in_one_move('o')
                self.board[y][x] = 'o'
            elif self.can_win_in_one_move('x'):
                y, x = self.can_win_in_one_move('x')
                self.board[y][x] = 'o'
            elif self.board[1][1] == 0:
                self.board[1][1] = 'o'
            else:
                move = False
                for x in range(self.width):
                    for y in range(self.height):
                        if self.board[y][x] == 0:
                            self.board[y][x] = 'o'
                            move = True
                            break
                    if move:
                        break
            self.change_player()

    def change_color_cheme(self, screen):
        """Смена цветовой схемы"""
        self.main_color, self.sub_color = self.sub_color, self.main_color
        self.render(screen)
