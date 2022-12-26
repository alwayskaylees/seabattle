import pygame, sys

size = 25
board = 3
width = size * 21 + board * 20
height = size * 11 + board * 10
pygame.init()

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('sea battle')
font = pygame.font.SysFont("notosans", 20)
sheet1 = [[0] * 15 for i in range(15)]
sheet2 = [[0] * 10 for i in range(10, 21)]


def greed():
    let = ["J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]
    for row in range(1, 11):

        for col in range(11, 21):
            x = col * size + (col + 1) * board

            y = row * size + (row + 1) * board

            pygame.draw.rect(screen, "white", (x, y, size, size))

        num = font.render(str(row), True, "red")
        letters = font.render(let[row - 1], True, "red")
        screen.blit(num, (x - 273, y + 4))

        screen.blit(letters, ((x + 5) - (row - 1) * 28, (y + 5) - (row) * 28))
        screen.blit(letters, ((x - 300) - (row - 1) * 28, (y + 5) - (row) * 28))

    for row in range(1, 11):

        for col in range(10):
            x = col * size + (col + 1) * board

            y = row * size + (row + 1) * board

            pygame.draw.rect(screen, "white", (x, y, size, size))

            if sheet1[row][col] == 'x':
                pygame.draw.circle(screen, "green", (x + size // 2, y + size // 2), size // 2 - 3)


def main():
    game_over = False
    screen.fill("black")

    while not game_over:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                sys.exit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                x_mouse, y_mouse = pygame.mouse.get_pos()

                col = x_mouse // (size + board)

                row = y_mouse // (size + board)

                if sheet1[row][col] == 0:
                    q = 1
                    if col + 1 == 1:
                        c = "A"
                    elif col + 1 == 2:
                        c = "B"
                    elif col + 1 == 3:
                        c = "C"
                    elif col + 1 == 4:
                        c = "D"
                    elif col + 1 == 5:
                        c = "E"
                    elif col + 1 == 6:
                        c = "F"
                    elif col + 1 == 7:
                        c = "G"
                    elif col + 1 == 8:
                        c = "H"
                    elif col + 1 == 9:
                        c = "I"
                    elif col + 1 == 10:
                        c = "J"
                    print(c, row)

                    if q == 1:
                        sheet1[row][col] = 'x'  # green

        greed()
        pygame.display.update()


main()
pygame.quit()