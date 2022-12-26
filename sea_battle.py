import pygame, sys

size = 25
board = 3
width = size * 21 + board * 20
height = size * 11 + board * 10
pygame.init()
# sheet1 = [[0]*15 for i in range(15)]
# sheet2 = [[0]*10 for i in range(10,21)]
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('sea battle')
font = pygame.font.SysFont("notosans", 25)
sheet1 = [[0] * 15 for i in range(15)]
sheet2 = [[0] * 10 for i in range(10, 21)]


def greed():
    for row in range(1, 11):

        for col in range(11, 21):
            x = col * size + (col + 1) * board

            y = row * size + (row + 1) * board

            pygame.draw.rect(screen, "white", (x, y, size, size))

        num = font.render(str(row), True, "red")
    #       screen.blit(num(x,y))

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
                    print(row, col)

                    if q == 1:
                        sheet1[row][col] = 'x'  # green

        greed()
        pygame.display.update()


main()
pygame.quit()
