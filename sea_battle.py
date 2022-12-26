import pygame

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


def main():
    game_over = False
    screen.fill("black")

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        greed()
        pygame.display.update()


main()
pygame.quit()
