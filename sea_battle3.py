import pygame as py
import sys
import os


class Screen():

    def __init__(self, title):
        self.height = 445
        self.title = title
        self.width = 440
        self.fill = (0, 0, 255)
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

    def focusCheck(self, mousepos, mouseclick):
        if (mousepos[0] >= self.x) and (mousepos[0] <= self.x + self.sx) and (mousepos[1] >= self.y) and (mousepos[
                                                                                                              1] <= self.y + self.sy):
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
                     ("white"), "Start Game")
MENU_BUTTON2 = Button(185, 55, 130, 50, ("white"),
                      ("white"), "TimesNewRoman",
                      ("black"), "Let's play sea battle")
MENU_BUTTON3 = Button(150, 220, 120, 50, ("black"),
                      ("black"), "TimesNewRoman",
                      ("white"), "Quit Game")
QUIT_BUTTON = Button(150, 300, 120, 50, ("black"),
                     ("black"), "TimesNewRoman",
                     ("red"), "Quit")
QUIT_BUTTON2 = Button(100, 55, 230, 150, ("white"),
                      ("white"), "TimesNewRoman",
                      ("red"), "Goodbye")

done = False
while not done:
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
        sheet1 = [[0] * 15 for i in range(15)]
        sheet2 = [[0] * 10 for i in range(10, 21)]


        def button():
            pass  # Нужно сделать нормальную кнопку

        def greed():
            let = ["J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]
            for row in range(1, 11):
                for col in range(10):
                    x = col * size + (col + 1) * board + 300
                    y = row * size + (row + 1) * board
                    py.draw.rect(screen, "white", (x, y, size, size))
                    if sheet2[row][col] == 'z':
                        py.draw.circle(screen, "red", (x + size // 2, y + size // 2), size // 2 - 3)
                num = font.render(str(row), True, "red")
                letters = font.render(let[row - 1], True, "red")
                screen.blit(num, (x - 273, y + 4))
                screen.blit(letters, ((x + 5) - (row - 1) * 28, (y + 5) - row * 28))
                screen.blit(letters, ((x - 300) - (row - 1) * 28, (y + 5) - row * 28))
            for row in range(1, 11):
                for col in range(10):
                    x = col * size + (col + 1) * board
                    y = row * size + (row + 1) * board
                    py.draw.rect(screen, "white", (x, y, size, size))
                    if sheet1[row][col] == 'x':
                        py.draw.circle(screen, "green", (x + size // 2, y + size // 2), size // 2 - 3)


        def main():
            game_over = False
            fon = py.transform.scale(load_image('fon.jpg'), (585, 445))
            screen.blit(fon, (0, 0))
            print("Game started.")
            while not game_over:
                for event in py.event.get():
                    if event.type == py.QUIT:
                        py.quit()
                        sys.exit(0)
                    elif event.type == py.MOUSEBUTTONDOWN:
                        x_mouse, y_mouse = py.mouse.get_pos()
                        if x_mouse > 310:
                            col = (x_mouse - 300) // (size + board)
                        else:
                            col = x_mouse // (size + board)
                        row = y_mouse // (size + board)
                        if (sheet1[row][col] == 0) and ((280 > x_mouse > 5) or (310 < x_mouse < 585)) and (
                                0 <= row <= 10) and (0 <= col <= 10):
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
                            if 3 < x_mouse < 280:
                                sheet1[row][col] = 'x'  # green
                            elif 310 < x_mouse < 585:
                                sheet2[row][col] = 'z'  # red
                        else:
                            print('None')

                greed()
                button()
                py.display.update()


        main()
        game_window.endCurrentScreen()
        win = menuScreen.makeCurrentScreen()

    for event in py.event.get():
        if (event.type == py.QUIT):
            done = True

    py.display.update()
py.quit()
