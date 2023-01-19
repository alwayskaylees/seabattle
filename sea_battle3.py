import pygame as py
import sys
import os
import random
import copy


class Screen:

    def __init__(self, title):
        self.screen = None
        self.height = 445
        self.title = title
        self.width = 440
        self.fill = (0, 0, 255)
        self.CurrentState = False

    def make_current_screen(self):
        py.display.set_caption(self.title)
        self.CurrentState = True
        self.screen = py.display.set_mode((self.width,
                                           self.height))

    def end_current_screen(self):
        self.CurrentState = False

    def check_update(self, fill):
        self.fill = fill
        return self.CurrentState

    def screen_update(self):
        if self.CurrentState:
            self.screen.fill(self.fill)

    def return_title(self):
        return self.screen


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = py.image.load(fullname).convert()
    except py.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Button:
    def __init__(self, x, y, sx, sy, bcolour,
                 fbcolour, tfont, fcolour, text):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.fontsize = 25
        self.bcolour = bcolour
        self.fbcolour = fbcolour
        self.fcolour = fcolour
        self.text = text
        self.CurrentState = False
        self.buttonf = py.font.SysFont(tfont, self.fontsize)

    def show_button(self, display):
        if self.CurrentState:
            py.draw.rect(display, self.fbcolour,
                         (self.x, self.y,
                          self.sx, self.sy))
        else:
            py.draw.rect(display, self.fbcolour,
                         (self.x, self.y,
                          self.sx, self.sy))
        textsurface = self.buttonf.render(self.text,
                                          False, self.fcolour)
        display.blit(textsurface,
                     ((self.x + (self.sx / 2) -
                       (self.fontsize / 2) * (len(self.text) / 2) -
                       5, (self.y + (self.sy / 2) -
                           (self.fontsize / 2) - 4))))

    def focus_check(self, mousepos, mouseclick):
        if self.x <= mousepos[0] <= self.x + self.sx and self.y <= mousepos[1] <= self.y + self.sy:
            self.CurrentState = True
            return mouseclick[0]
        else:
            self.CurrentState = False
            return False


class AutoShips:

    def __init__(self, offset):
        self.offset = offset
        self.available_blocks = {(x, y) for x in range(
            1 + self.offset, 11 + self.offset) for y in range(1, 11)}
        self.ships_set = set()
        self.ships = self.populate_grid()
        self.orientation = None
        self.direction = None

    def __create_start_block(self, available_blocks):
        self.orientation = random.randint(0, 1)
        # -1 is left or down, 1 is right or up
        self.direction = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, self.orientation, self.direction

    def __create_ship(self, number_of_blocks, available_blocks):
        ship_coordinates = []
        x, y, self.orientation, self.direction = self.__create_start_block(
            available_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if not self.orientation:
                self.direction, x = self.__get_new_block_for_ship(
                    x, self.direction, self.orientation, ship_coordinates)
            else:
                self.direction, y = self.__get_new_block_for_ship(
                    y, self.direction, self.orientation, ship_coordinates)
        if self.__is_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.__create_ship(number_of_blocks, available_blocks)

    def __get_new_block_for_ship(self, coor, direction, orientation, ship_coordinates):
        self.direction = direction
        self.orientation = orientation
        if (coor <= 1 - self.offset * (self.orientation - 1) and self.direction == -1) or (
                coor >= 10 - self.offset * (self.orientation - 1) and self.direction == 1):
            self.direction *= -1
            return self.direction, ship_coordinates[0][self.orientation] + self.direction
        else:
            return self.direction, ship_coordinates[-1][self.orientation] + self.direction

    def __is_ship_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def __add_new_ship_to_set(self, new_ship):
        self.ships_set.update(new_ship)

    def __update_available_blocks_for_creating_ships(self, new_ship):
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if self.offset < (elem[0] + k) < 11 + self.offset and 0 < (elem[1] + m) < 11:
                        self.available_blocks.discard(
                            (elem[0] + k, elem[1] + m))

    def populate_grid(self):
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5 - number_of_blocks):
                new_ship = self.__create_ship(
                    number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.__add_new_ship_to_set(new_ship)
                self.__update_available_blocks_for_creating_ships(new_ship)
        print('Для разработчиков! Координаты кораблей бота -', ships_coordinates_list)  # потом убрать(сделано для удобства)
        return ships_coordinates_list


py.init()
py.font.init()

menuScreen = Screen("Menu Screen")
game_window = Screen("Control")
window = Screen("Exit")
menuScreen.make_current_screen()
MENU_BUTTON = Button(150, 150, 120, 50, "black",
                     "black", "TimesNewRoman",
                     "white", "New game")
MENU_BUTTON2 = Button(185, 55, 130, 50, "white",
                      "white", "TimesNewRoman",
                      "black", "Let's play sea battle")
MENU_BUTTON3 = Button(150, 220, 120, 50, "black",
                      "black", "TimesNewRoman",
                      "white", "Quit")
QUIT_BUTTON = Button(150, 300, 120, 50, "black",
                     "black", "TimesNewRoman",
                     "red", "Quit")
QUIT_BUTTON2 = Button(100, 55, 230, 150, "white",
                      "white", "TimesNewRoman",
                      "red", "Goodbye")

done = False
while not done:  # смена экранов
    menuScreen.screen_update()
    game_window.screen_update()
    window.screen_update()
    mouse_pos = py.mouse.get_pos()
    mouse_click = py.mouse.get_pressed()
    keys = py.key.get_pressed()
    if menuScreen.check_update((255, 255, 255)):
        start_button = MENU_BUTTON.focus_check(mouse_pos, mouse_click)
        quit_button = MENU_BUTTON3.focus_check(mouse_pos, mouse_click)
        MENU_BUTTON.show_button(menuScreen.return_title())
        MENU_BUTTON2.show_button(menuScreen.return_title())
        MENU_BUTTON3.show_button(menuScreen.return_title())
        if start_button:
            game_window.make_current_screen()
            menuScreen.end_current_screen()
        if quit_button:
            window.make_current_screen()
            menuScreen.end_current_screen()

    elif window.check_update((255, 255, 255)):
        exit_button = QUIT_BUTTON.focus_check(mouse_pos, mouse_click)
        QUIT_BUTTON.show_button(window.return_title())
        QUIT_BUTTON2.show_button(window.return_title())
        if exit_button:
            sys.exit()

    elif game_window.check_update((255, 255, 255)):
        size = 25
        board = 3
        width = size * 21 + board * 20
        height = size * 15 + board * 10
        py.init()
        screen = py.display.set_mode((width, height))
        py.display.set_caption('Sea Battle')
        font = py.font.SysFont("notosans", 20)
        font3 = py.font.SysFont("notosans", 40)
        cells = [f"{i}-{j}" for i in range(1, 11) for j in range(1, 11)]
        sheet = [[0] * 21 for i in range(21)]  # два поля вместе


        def button():
            py.draw.rect(screen, "white", (5, 336, 80, 40))
            num3 = font3.render("Menu", True, "black")
            screen.blit(num3, (7, 343))
            py.draw.rect(screen, "white", (505, 336, 77, 40))
            num3 = font3.render("Start", True, "black")
            screen.blit(num3, (510, 343))


        def greed():
            let = ["J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]
            for row in range(1, 11):  # второе поле
                for col in range(11, 21):
                    x = col * size + (col + 1) * board
                    y = row * size + (row + 1) * board
                    py.draw.rect(screen, "white", (x, y, size, size))
                    if sheet[row][col] == 'z':  # рисует красный кружок
                        py.draw.circle(screen, "red", (x + size // 2, y + size // 2), size // 2 - 3)
                    if sheet[row][col] == 'b':  # рисует черный кружок
                        py.draw.circle(screen, "black", (x + size // 2, y + size // 2), size // 2 + 1)
                num = font.render(str(row), True, "red")  # цифры
                letters = font.render(let[row - 1], True, "red")
                screen.blit(num, (x - 273, y + 4))
                screen.blit(letters, ((x + 5) - (row - 1) * 28, (y + 5) - row * 28))  # буквы на 1 поле
                screen.blit(letters, ((x - 300) - (row - 1) * 28, (y + 5) - row * 28))  # буквы на 2 поле
            for row in range(1, 11):  # первое поле
                for col in range(10):
                    x = col * size + (col + 1) * board
                    y = row * size + (row + 1) * board
                    py.draw.rect(screen, "white", (x, y, size, size))
                    if sheet[row][col] == 'x':  # рисует синий кружок
                        py.draw.circle(screen, "blue", (x + size // 2, y + size // 2), size // 2 - 3)
                    if sheet[row][col] == 'b':  # рисует черный кружок
                        py.draw.circle(screen, "black", (x + size // 2, y + size // 2), size // 2 + 1)


        def main():
            global computer_ships_working
            ship_left_first = 20
            ship_left_second = 20
            gamestarted = False
            moving11, moving12, moving13, moving14 = False, False, False, False
            moving21, moving22, moving23 = False, False, False
            moving31, moving32, moving41 = False, False, False
            game_over = False
            fon = py.transform.scale(load_image('fon.jpg'), (585, 445))
            screen.blit(fon, (0, 0))
            x11, y11 = 115, 320  # корабли 1 клетка
            x11_new, y11_new = 0, 0
            x12, y12 = 115, 360
            x12_new, y12_new = 0, 0
            x13, y13 = 152, 320
            x13_new, y13_new = 0, 0
            x14, y14 = 152, 360
            x14_new, y14_new = 0, 0
            x21, y21 = 190, 320  # корабли в 2 клетки
            x21_new, y21_new = 0, 0
            x22, y22 = 190, 360
            x22_new, y22_new = 0, 0
            x23, y23 = 253, 320
            x23_new, y23_new = 0, 0
            x31, y31 = 253, 360
            x31_new, y31_new = 0, 0
            x32, y32 = 345, 360
            x32_new, y32_new = 0, 0
            x41, y41 = 317, 320
            x41_new, y41_new = 0, 0
            up1, up2, up3, up4, up5, up6 = False, False, False, False, False, False
            player_turn = True
            while not game_over:
                x_mouse, y_mouse = py.mouse.get_pos()
                col = x_mouse // (size + board)
                row = y_mouse // (size + board)
                for event in py.event.get():
                    if event.type == py.QUIT:
                        game_over = True
                    if event.type == py.MOUSEBUTTONDOWN and event.button == 1:  #
                        if sheet[row][col] == 0:
                            if col == 0 and row == 12 or col == 1 and row == 12 or col == 2 and row == 12 or col == 0 \
                                    and row == 11:
                                game_over = True  # кнопка menu активируется и выходит из окна игры
                                gamestarted = False
                            if col == 19 and row == 12 or col == 20 and row == 12 or col == 21 and row == 12 or \
                                    col == 20 and row == 11:
                                if (x11 > 310 and y11 < 284 and x12 > 310 and y12 < 284 and x13 > 310 and y13 < 284 and
                                        x14 > 310 and y14 < 284 and x21 > 310 and y21 < 284 and x22 > 310 and y22 < 284
                                        and x23 > 310 and y23 < 284 and x31 > 310 and y31 < 284 and x32 > 310 and
                                        y32 < 284 and x41 > 310 and y41 < 284):
                                    print("Game started.")
                                    gamestarted = True
                                    computer = AutoShips(0)
                                    computer_ships_working = copy.deepcopy(computer.ships)
                                    ships_our = [[(x11 - 3) // 28, (y11 - 3) // 28], [(x12 - 3) // 28, (y12 - 3) // 28],
                                                 [(x13 - 3) // 28, (y13 - 3) // 28],
                                                 [(x14 - 3) // 28, (y14 - 3) // 28],
                                                 [((x21 - 3) // 28, (y21 - 3) // 28),
                                                  (((x21 - 3) // 28) + 1,
                                                   (y21 - 3) // 28)],
                                                 [((x22 - 3) // 28, (y22 - 3) // 28),
                                                  (((x22 - 3) // 28) + 1, (y22 - 3) // 28)],
                                                 [((x23 - 3) // 28, (y23 - 3) // 28),
                                                  (((x23 - 3) // 28) + 1, (y23 - 3) // 28)],
                                                 [((x31 - 3) // 28, (y31 - 3) // 28),
                                                  (((x31 - 3) // 28) + 1, (y31 - 3) // 28),
                                                  (((x31 - 3) // 28) + 2, (y31 - 3) // 28)],
                                                 [((x32 - 3) // 28, (y32 - 3) // 28),
                                                  (((x32 - 3) // 28) + 1, (y32 - 3) // 28),
                                                  (((x32 - 3) // 28) + 2, (y32 - 3) // 28)],
                                                 [((x41 - 3) // 28, (y41 - 3) // 28),
                                                  (((x41 - 3) // 28) + 1, (y41 - 3) // 28),
                                                  (((x41 - 3) // 28) + 2, (y41 - 3) // 28),
                                                  (((x41 - 3) // 28) + 3, (y41 - 3) // 28)]]
                                    print('Для разработчиков! Координаты кораблей игрока -', ships_our)  # потом убрать(сделано для удобства)
                                else:
                                    print("Корабли вне поля!")
                    if event.type == py.MOUSEBUTTONDOWN and event.button == 1 and gamestarted:  # рисование синих
                        # и красных кружков на 1 и 2 поле
                        if sheet[row][col] == 0 and player_turn:
                            if col < 10 and row < 11:
                                if col == 0:
                                    c = "A"
                                elif col == 1:
                                    c = "B"
                                elif col == 2:
                                    c = "C"
                                elif col == 3:
                                    c = "D"
                                elif col == 4:
                                    c = "E"
                                elif col == 5:
                                    c = "F"
                                elif col == 6:
                                    c = "G"
                                elif col == 7:
                                    c = "H"
                                elif col == 8:
                                    c = "I"
                                elif col == 9:
                                    c = "J"
                                print('Вы совершили выстрел по координатам', c, '-', row)
                                check = False
                                ships = computer_ships_working
                                for i in ships:
                                    for j in i:
                                        if j == (row, col + 1):
                                            sheet[row][col] = 'b'  # black
                                            check = True
                                            ship_left_first -= 1
                                            print("Часть корабля или весь корабль противника были разрушены!")
                                if not check:
                                    sheet[row][col] = 'x'  # blue
                                    print("Вы не попали по вражеским кораблям!")
                                player_turn = False
                                if ship_left_first == 0:
                                    print('---')
                                    print('---')
                                    print('Хорошая работа, командир! Вы победили в этом сражении!')
                                    print('Противнику оставалось потопить еще', ship_left_second, 'частей кораблей')
                                    game_over = True
                                if ship_left_second == 0:
                                    print('---')
                                    print('---')
                                    print('О нет... командир... мы потерпели поражение')
                                    print('Вам оставалось потопить еще', ship_left_first, 'частей кораблей противника')
                                    game_over = True
                            if not player_turn and gamestarted:
                                check = False
                                fire = random.choice(cells)
                                cells.remove(fire)
                                fire_coordinates = fire.split('-')
                                row = int(fire_coordinates[0])
                                col = int(fire_coordinates[1]) + 10
                                if int(fire_coordinates[1]) == 1:
                                    c = "A"
                                elif int(fire_coordinates[1]) == 2:
                                    c = "B"
                                elif int(fire_coordinates[1]) == 3:
                                    c = "C"
                                elif int(fire_coordinates[1]) == 4:
                                    c = "D"
                                elif int(fire_coordinates[1]) == 5:
                                    c = "E"
                                elif int(fire_coordinates[1]) == 6:
                                    c = "F"
                                elif int(fire_coordinates[1]) == 7:
                                    c = "G"
                                elif int(fire_coordinates[1]) == 8:
                                    c = "H"
                                elif int(fire_coordinates[1]) == 9:
                                    c = "I"
                                elif int(fire_coordinates[1]) == 10:
                                    c = "J"
                                print('Противник совершил выстрел по координатам', c, '-', int(fire_coordinates[0]))
                                for i in ships_our:
                                    for j in i:
                                        if j == (col, row):
                                            sheet[row][col] = 'b'  # black
                                            check = True
                                            print("Часть вашего корабля или весь ваш корабль были разрушены!")
                                            ship_left_second -= 1
                                if not check:
                                    sheet[row][col] = 'z'  # blue
                                    print("Все ваши корабли остались в том же состоянии, что и до выстрела противника!")
                                player_turn = True
                                if ship_left_first == 0:
                                    print('---')
                                    print('---')
                                    print('Хорошая работа, командир! Вы победили в этом сражении!')
                                    print('Противнику оставалось потопить еще', ship_left_second, 'частей кораблей')
                                    game_over = True
                                if ship_left_second == 0:
                                    print('---')
                                    print('---')
                                    print('О нет... командир... противник сумел разгромить наш флот')
                                    print('Вам оставалось потопить еще', ship_left_first, 'частей кораблей противника')
                                    game_over = True
                                if not game_over:
                                    print('...ожидание следующих действий...')
                    if event.type == py.MOUSEBUTTONDOWN and event.button == 1 and not gamestarted:  # перемещение
                        # кораблей
                        if x11 < event.pos[0] < x11 + 25 and y11 < event.pos[1] < y11 + 25:
                            moving11 = True
                        if x12 < event.pos[0] < x12 + 25 and y12 < event.pos[1] < y12 + 25:
                            moving12 = True
                        if x13 < event.pos[0] < x13 + 25 and y13 < event.pos[1] < y13 + 25:
                            moving13 = True
                        if x14 < event.pos[0] < x14 + 25 and y14 < event.pos[1] < y14 + 25:
                            moving14 = True
                        if x21 < event.pos[0] < x21 + 50 and y21 < event.pos[1] < y21 + 25:
                            moving21 = True
                        if x22 < event.pos[0] < x22 + 50 and y22 < event.pos[1] < y22 + 25:
                            moving22 = True
                        if x23 < event.pos[0] < x23 + 50 and y23 < event.pos[1] < y23 + 25:
                            moving23 = True
                        if x31 < event.pos[0] < x31 + 81 and y31 < event.pos[1] < y31 + 25:
                            moving31 = True
                        if x32 < event.pos[0] < x32 + 81 and y32 < event.pos[1] < y32 + 25:
                            moving32 = True
                        if x41 < event.pos[0] < x41 + 109 and y41 < event.pos[1] < y41 + 25:
                            moving41 = True
                    if event.type == py.MOUSEMOTION and x_mouse < 563 and y_mouse > 31:  # продолжение перемещения
                        # кораблей
                        x_mouse, y_mouse = py.mouse.get_pos()
                        col = x_mouse // (size + board)
                        row = y_mouse // (size + board)
                        x = col * size + (col + 1) * board
                        y = row * size + (row + 1) * board
                        if sheet[row][col] == 0:
                            if row > 10 or col > 10:
                                if moving11:
                                    x11_new, y11_new = event.rel
                                    x11, y11 = x11 + x11_new, y11 + y11_new
                                    x11, y11 = x, y
                                if moving12:
                                    x12_new, y12_new = event.rel
                                    x12, y12 = x12 + x12_new, y12 + y12_new
                                    x12, y12 = x, y
                                if moving13:
                                    x13_new, y13_new = event.rel
                                    x13, y13 = x13 + x13_new, y13 + y13_new
                                    x13, y13 = x, y
                                if moving14:
                                    x14_new, y14_new = event.rel
                                    x14, y14 = x14 + x14_new, y14 + y14_new
                                    x14, y14 = x, y
                                if moving21:
                                    x21_new, y21_new = event.rel
                                    x21, y21 = x21 + x21_new, y21 + y21_new
                                    x21, y21 = x, y
                                if moving22:
                                    x22_new, y22_new = event.rel
                                    x22, y22 = x22 + x22_new, y22 + y22_new
                                    x22, y22 = x, y
                                if moving23:
                                    x23_new, y23_new = event.rel
                                    x23, y23 = x23 + x23_new, y23 + y23_new
                                    x23, y23 = x, y
                                if moving31:
                                    x31_new, y31_new = event.rel
                                    x31, y31 = x31 + x31_new, y31 + y31_new
                                    x31, y31 = x, y
                                if moving32:
                                    x32_new, y32_new = event.rel
                                    x32, y32 = x32 + x32_new, y32 + y32_new
                                    x32, y32 = x, y
                                if moving41:
                                    x41_new, y41_new = event.rel
                                    x41, y41 = x41 + x41_new, y41 + y41_new
                                    x41, y41 = x, y
                    if event.type == py.MOUSEBUTTONUP and event.button == 1:  # продолжение перемещения кораблей
                        moving11, moving12, moving13, moving14, moving21 = False, False, False, False, False
                        moving22, moving23, moving31, moving32, moving41 = False, False, False, False, False
                py.draw.rect(screen, "blue", (x22 + 4, y22 + 4, 53 - 8, size - 8))  # не убираю разность чисел и не пишу сразу ответ, чтобы потом не
                py.draw.rect(screen, "blue", (x21 + 4, y21 + 4, 53 - 8, size - 8))  # запутаться и если что вернуть изначальные числа назад
                py.draw.rect(screen, "blue", (x11 + 4, y11 + 4, size - 8, size - 8))
                py.draw.rect(screen, "blue", (x12 + 4, y12 + 4, size - 8, size - 8))
                py.draw.rect(screen, "blue", (x13 + 4, y13 + 4, size - 8, size - 8))
                py.draw.rect(screen, "blue", (x14 + 4, y14 + 4, size - 8, size - 8))
                py.draw.rect(screen, "blue", (x23 + 4, y23 + 4, 53 - 8, size - 8))
                py.draw.rect(screen, "blue", (x31 + 4, y31 + 4, 81 - 8, size - 8))
                py.draw.rect(screen, "blue", (x32 + 4, y32 + 4, 81 - 8, size - 8))
                py.draw.rect(screen, "blue", (x41 + 4, y41 + 4, 109 - 8, size - 8))
                py.display.flip()
                screen.blit(fon, (0, 0))
                greed()
                button()


        main()
        game_window.end_current_screen()
        menuScreen.make_current_screen()
    for event in py.event.get():
        if event.type == py.QUIT:
            done = True
    py.display.update()
py.quit()
