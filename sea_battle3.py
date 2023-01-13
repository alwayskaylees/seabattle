import pygame as py
import sys


class Screen():

    def __init__(self, title, width=440, height=445,
                 fill=(0, 0, 255)):
        self.height = height
        self.title = title
        self.width = width
        self.fill = fill
        self.CurrentState = False

    def makeCurrentScreen(self):
        py.display.set_caption(self.title)
        self.CurrentState = True
        self.screen = py.display.set_mode((self.width,
                                           self.height))

    def endCurrentScreen(self):
        self.CurrentState = False

    def checkUpdate(self, fill):
        self.fill = fill
        return self.CurrentState

    def screenUpdate(self):
        if self.CurrentState:
            self.screen.fill(self.fill)

    def returnTitle(self):
        return self.screen


class Button():
    def __init__(self, x, y, sx, sy, bcolour,
                 fbcolour, font, fcolour, text):
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
        self.buttonf = py.font.SysFont(font, self.fontsize)

    def showButton(self, display):
        if (self.CurrentState):
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

    def focusCheck(self, mousepos, mouseclick):
        if (mousepos[0] >= self.x and mousepos[0] <= self.x +
                self.sx and mousepos[1] >= self.y and mousepos[1]
                <= self.y + self.sy):
            self.CurrentState = True
            return mouseclick[0]
        else:
            self.CurrentState = False
            return False


py.init()
py.font.init()

menuScreen = Screen("Menu Screen")
game_window = Screen("Control")
window = Screen("Exit")
win = menuScreen.makeCurrentScreen()
MENU_BUTTON = Button(150, 150, 120, 50, ("black"),
                     ("black"), "TimesNewRoman",
                     ("white"), "New game")
MENU_BUTTON2 = Button(185, 55, 130, 50, ("white"),
                      ("white"), "TimesNewRoman",
                      ("black"), "Let's play sea battle")
MENU_BUTTON3 = Button(150, 220, 120, 50, ("black"),
                      ("black"), "TimesNewRoman",
                      ("white"), "Quit")
QUIT_BUTTON = Button(150, 300, 120, 50, ("black"),
                     ("black"), "TimesNewRoman",
                     ("red"), "Quit")
QUIT_BUTTON2 = Button(100, 55, 230, 150, ("white"),
                      ("white"), "TimesNewRoman",
                      ("red"), "Goodbye")

done = False
while not done:  # смена экранов
    menuScreen.screenUpdate()
    game_window.screenUpdate()
    window.screenUpdate()
    mouse_pos = py.mouse.get_pos()
    mouse_click = py.mouse.get_pressed()
    keys = py.key.get_pressed()
    if menuScreen.checkUpdate((255, 255, 255)):
        start_button = MENU_BUTTON.focusCheck(mouse_pos,
                                              mouse_click)
        quit_button = MENU_BUTTON3.focusCheck(mouse_pos,
                                              mouse_click)
        MENU_BUTTON.showButton(menuScreen.returnTitle())
        MENU_BUTTON2.showButton(menuScreen.returnTitle())
        MENU_BUTTON3.showButton(menuScreen.returnTitle())
        if start_button:
            win = game_window.makeCurrentScreen()
            menuScreen.endCurrentScreen()
        if quit_button:
            win = window.makeCurrentScreen()
            menuScreen.endCurrentScreen()

    elif window.checkUpdate((255, 255, 255)):
        exit_button = QUIT_BUTTON.focusCheck(mouse_pos,
                                             mouse_click)
        QUIT_BUTTON.showButton(window.returnTitle())
        QUIT_BUTTON2.showButton(window.returnTitle())
        if exit_button:
            sys.exit()

    elif game_window.checkUpdate((255, 255, 255)):
        size = 25
        board = 3
        width = size * 21 + board * 20
        height = size * 15 + board * 10
        py.init()
        screen = py.display.set_mode((width, height))
        py.display.set_caption('sea battle')
        font = py.font.SysFont("notosans", 20)
        font3 = py.font.SysFont("notosans", 40)
        sheet = [[0] * 21 for i in range(21)]  # два поля вместе


        def button():
            py.draw.rect(screen, "white", (5, 336, 80, 40))
            num3 = font3.render("Menu", True, "black")
            screen.blit(num3, (7, 343))


        def greed():
            let = ["J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]

            for row in range(1, 11):  # второе поле
                for col in range(11, 21):
                    x = col * size + (col + 1) * board
                    y = row * size + (row + 1) * board
                    py.draw.rect(screen, "white", (x, y, size, size))
                num = font.render(str(row), True, "red")  # цифры
                letters = font.render(let[row - 1], True, "red")
                screen.blit(num, (x - 273, y + 4))
                screen.blit(letters, ((x + 5) - (row - 1) * 28, (y + 5) - (row) * 28))  # буквы на 1 поле
                screen.blit(letters, ((x - 300) - (row - 1) * 28, (y + 5) - (row) * 28))  # буквы на 2 поле

            for row in range(1, 11):  # первое поле
                for col in range(10):
                    x = col * size + (col + 1) * board
                    y = row * size + (row + 1) * board
                    py.draw.rect(screen, "white", (x, y, size, size))
                    if sheet[row][col] == 'x':  # рисует зеленый кружок
                        py.draw.circle(screen, "green", (x + size // 2, y + size // 2), size // 2 - 3)


        def main():
            moving11, moving12, moving13, moving14 = False, False, False, False
            moving21, moving22, moving23 = False, False, False
            game_over = False
            screen.fill("black")
            x11, y11 = 115, 320  # корабли 1 клетка
            x11_new, y11_new = 0, 0
            x12, y12 = 115, 360
            x12_new, y12_new = 0, 0
            x13, y13 = 150, 320
            x13_new, y13_new = 0, 0
            x14, y14 = 150, 360
            x14_new, y14_new = 0, 0
            x21, y21 = 190, 320  # корабли в 2 клетки
            x21_new, y21_new = 0, 0
            x22, y22 = 190, 360
            x22_new, y22_new = 0, 0
            x23, y23 = 253, 320
            x23_new, y23_new = 0, 0

            print("new game")
            while not game_over:
                for event in py.event.get():
                    if event.type == py.QUIT:
                        game_over = True
                    if event.type == py.MOUSEBUTTONDOWN and event.button == 1:  # рисование зеленых кружков на 1 поле
                        x_mouse, y_mouse = py.mouse.get_pos()
                        col = x_mouse // (size + board)
                        row = y_mouse // (size + board)
                        if sheet[row][col] == 0:
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
                                print(c, row)
                                sheet[row][col] = 'x'  # green
                            if col == 0 and row == 12 or col == 1 and row == 12 or col == 2 and row == 12 or col == 0 and row == 11:
                                game_over = True  # кнопка menu активируется  и выходит из окна игры
                    if event.type == py.MOUSEBUTTONDOWN and event.button == 1:  # перемещение кораблей
                        if x11 < event.pos[0] < x11 + 25 and y11 < event.pos[1] < y11 + 25:
                            moving11 = True
                        if x12 < event.pos[0] < x12 + 25 and y12 < event.pos[1] < y12 + 25:
                            moving12 = True
                        if x13 < event.pos[0] < x13 + 25 and y13 < event.pos[1] < y13 + 25:
                            moving13 = True
                        if x14 < event.pos[0] < x14 + 25 and y14 < event.pos[1] < y14 + 25:
                            moving14 = True
                        if x21 < event.pos[0] < x21 + 25 and y21 < event.pos[1] < y21 + 25:
                            moving21 = True
                        if x22 < event.pos[0] < x22 + 25 and y22 < event.pos[1] < y12 + 25:
                            moving22 = True
                        if x23 < event.pos[0] < x23 + 25 and y23 < event.pos[1] < y23 + 25:
                            moving23 = True
                    if event.type == py.MOUSEMOTION:  # продолжение перемещения кораблей
                        if moving11:
                            x11_new, y11_new = event.rel
                            x11, y11 = x11 + x11_new, y11 + y11_new
                        if moving12:
                            x12_new, y12_new = event.rel
                            x12, y12 = x12 + x12_new, y12 + y12_new
                        if moving13:
                            x13_new, y13_new = event.rel
                            x13, y13 = x13 + x13_new, y13 + y13_new
                        if moving14:
                            x14_new, y14_new = event.rel
                            x14, y14 = x14 + x14_new, y14 + y14_new
                        if moving21:
                            x21_new, y21_new = event.rel
                            x21, y21 = x21 + x21_new, y21 + y21_new
                        if moving22:
                            x22_new, y22_new = event.rel
                            x22, y22 = x22 + x22_new, y22 + y22_new
                        if moving23:
                            x23_new, y23_new = event.rel
                            x23, y23 = x23 + x23_new, y23 + y23_new
                    if event.type == py.MOUSEBUTTONUP and event.button == 1:  # продолжение перемещения кораблей
                        moving11 = False
                        moving12 = False
                        moving13 = False
                        moving14 = False
                        moving21 = False
                        moving22 = False
                        moving23 = False
                py.draw.rect(screen, "red", (x11, y11, size, size))
                py.draw.rect(screen, "red", (x12, y12, size, size))
                py.draw.rect(screen, "red", (x13, y13, size, size))
                py.draw.rect(screen, "red", (x14, y14, size, size))
                py.draw.rect(screen, "red", (x21, y21, 53, size))
                py.draw.rect(screen, "red", (x22, y22, 53, size))
                py.draw.rect(screen, "red", (x23, y23, 53, size))
                py.display.flip()

                screen.fill((0, 0, 0))

                greed()
                button()


        main()
        game_window.endCurrentScreen()
        win = menuScreen.makeCurrentScreen()

    for event in py.event.get():
        if (event.type == py.QUIT):
            done = True

    py.display.update()
py.quit()
