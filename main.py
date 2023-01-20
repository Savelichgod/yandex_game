import pygame

from TicTacToe import *
from dbFunc import *

game_started = False


class MenuItem:
    """Создание пункта меню"""

    def __init__(self, text, y):
        self.font = pygame.font.SysFont('Arial', 40)
        self.text = text
        self.color = (0, 0, 255)
        self.item = self.font.render(self.text, True, self.color)
        self.x = width // 2 - self.item.get_size()[0] // 2
        self.y = y

    def point_inside(self, pos):
        """Находится ли точка на пункте меню"""
        x, y = pos
        width, height = self.item.get_size()
        return self.x <= x <= self.x + width and self.y <= y <= self.y + height

    def draw(self, screen):
        """Выводим пункт меню на экран"""
        self.item = self.font.render(self.text, True, self.color)
        screen.blit(self.item, (self.x, self.y))

    def hover(self, pos):
        """Выделение пункта цветом при наведении"""
        if self.point_inside(pos):
            self.color = (255, 0, 0)
        else:
            self.color = (0, 0, 255)
        self.draw(screen)

    def click(self, pos):
        """Обработка нажатия на пункт меню"""
        global action
        if self.point_inside(pos):
            action = self.text


class Menu:
    def __init__(self):
        self.items = []
        self.dy = 40
        self.items.append(MenuItem('Войти', 0))
        self.items.append(MenuItem('Зарегистрироваться', self.items[-1].y + self.dy))
        self.items.append(MenuItem('Справка', self.items[-1].y + self.dy))
        self.items.append(MenuItem('Статистика', self.items[-1].y + self.dy))

    def draw(self, screen):
        """Отрисовка меню целиком"""
        screen.fill((255, 255, 255))
        for item in self.items:
            item.draw(screen)
        pygame.display.flip()

    def hover(self, pos):
        """Проверка надеведния на любой из пунктов"""
        for item in self.items:
            item.hover(pos)

    def click(self, pos):
        """Проверка клика на любой из пунктов"""
        for item in self.items:
            item.click(pos)


class Form:
    """Создание формы входа"""

    def __init__(self, fields_list):
        self.font = pygame.font.SysFont('Arial', 40)
        self.errors_font = pygame.font.SysFont('Arial', 20)
        self.fields = dict()
        for field in fields_list:
            self.fields[field] = ''
        self.selected = 0
        self.keys = list(self.fields.keys())
        self.active_key = 0
        self.errors = False

    """сделать активным следующее поле"""

    def next(self):
        if self.active_key < len(self.keys) - 1:
            self.active_key += 1
        self.draw(screen)

    """сделать активным предыщее поле"""

    def previos(self):
        if self.active_key > 0:
            self.active_key -= 1
        self.draw(screen)

    """получить активное поле"""

    def get_selected(self):
        return self.keys[self.active_key]

    """нарисовать всю форму"""

    def draw(self, screen):
        screen.fill((255, 255, 255))
        y = 0
        for field in self.fields:

            if field == self.get_selected():
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            screen.blit(self.font.render(field + ': ' + self.fields[field], True, color), (0, y))
            y += 50
        if self.errors:
            error_text = self.errors_font.render(f'{self.errors}', True,
                                                 (255, 0, 0))
            screen.blit(error_text, (0, height - 100))
        pygame.display.flip()

    def send_form(self):
        """абстрактный метод отправки формы"""
        pass

    def key_pressed(self, key_code):
        global action
        active_field = self.get_selected()
        if key_code == pygame.K_BACKSPACE:
            self.fields[active_field] = self.fields[active_field][:-1]
        elif key_code == 13:
            if active_field == self.keys[-1]:
                self.send_form()
            else:
                self.next()
        elif key_code == pygame.K_UP:
            self.previos()
        elif key_code == pygame.K_DOWN:
            self.next()
        else:
            try:
                self.fields[active_field] += chr(key_code)
            except Exception:
                print('Ошибка')


class LoginForm(Form):
    def send_form(self):
        global action
        global player_id
        id = login(self.fields['name'], self.fields['password'])
        if id:
            action = 'game'
            player_id = id
            self.errors = []
        else:
            self.errors = 'Ошибка в логине или пароле!'


class RegistrationForm(Form):
    def send_form(self):
        global action
        name = self.fields['name']
        password = self.fields['password']
        confirm = self.fields['confirm']
        if password != confirm:
            self.errors = 'Пароль и подвтерждение не совпадают'
        if not name or not password or not confirm:
            self.errors = 'Заполнены не все поля'
        if name in get_players():
            self.errors = f'Пользователь с именем {name} уже зарегистрирован!'
        if not self.errors:
            add_player(name, password)
            action = 'Меню'


def print_statistics(screen):
    screen.fill(pygame.Color('white'))
    results = get_statistics()
    font = pygame.font.SysFont(None, 40)
    padding_x = 20
    padding_y = 20
    for i in range(len(results)):
        name, score = results[i]
        text = f'{i + 1}) {name} {score}% побед'
        record = font.render(text, True, pygame.Color('black'))
        screen.blit(record, (padding_x, padding_y))
        padding_y += 40
    pygame.display.flip()


def print_help(screen):
    screen.fill(pygame.Color('white'))
    info = ['Нажмите ESC для выхода в главное меню', 'Нажмите "m" для смены цветовой схемы',
            'Нажмите "b" для смены режима бота']
    font = pygame.font.SysFont(None, 30)
    padding_x = 20
    padding_y = 20
    for i in range(len(info)):
        text = info[i]
        record = font.render(text, True, pygame.Color('black'))
        screen.blit(record, (padding_x, padding_y))
        padding_y += 40
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    running = True
    action = 'Меню'
    size = width, height = 500, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Крестики-нолики от Савелия')
    board = Board(3, 3)
    board.set_view(100, 50, 100)

    menu = Menu()
    login_form = LoginForm(['name', 'password'])
    registration_form = RegistrationForm(['name', 'password', 'confirm'])
    player_id = False

    while running:
        if action == 'Меню':
            menu.draw(screen)
        if action == 'Войти':
            login_form.draw(screen)
        if action == 'Справка':
            print_help(screen)
        if action == 'Зарегистрироваться':
            registration_form.draw(screen)
        if action == 'Статистика':
            print_statistics(screen)
        if action == 'game':
            board.render(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if action == 'Меню':
                    menu.hover(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if action == 'game':
                    board.player_move(event.pos)
                if action == 'Меню':
                    menu.click(event.pos)

            if event.type == pygame.KEYDOWN:
                # нажать ESC для выхода в меню
                if event.key == pygame.K_ESCAPE:
                    action = 'Меню'
                if action == 'game':
                    # нажать m для смены цветовой схемы
                    if event.key == pygame.K_m:
                        board.change_color_cheme(screen)
                        # нажать b чтобы включить/выключить режим бота
                    if event.key == pygame.K_b:
                        board.bot = not board.bot
                if action == 'Войти':
                    login_form.key_pressed(event.key)
                if action == 'Зарегистрироваться':
                    registration_form.key_pressed(event.key)

        if action == 'game':
            board.bot_move()
            board.render(screen)
            winer = board.is_game_over()
            if winer:
                print(player_id, winer.upper())
                board.show_game_result(winer, screen)
                if winer == '=':
                    write_game_result(player_id, "draw")
                else:
                    if winer.upper == 'X':
                        print('ура работает')
                        write_game_result(player_id, "won")
                    else:
                        write_game_result(player_id, "lose")

    pygame.quit()
