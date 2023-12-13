import pygame
import random
import sys


# Размер игрового поля
board_size = (10, 10)

# Цвета кружочков
circle_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]


def change_colors(board):
    for i in range(board_size[0]):
        for j in range(board_size[1]):
            board[i][j] = random.randint(0, len(circle_colors) - 1)


def main():
    # Игровое поле
    board = []
    for i in range(board_size[0]):
        board.append([0] * board_size[1])

    change_colors(board)

    # Инициализация PyGame
    pygame.init()

    # Создание окна игры
    screen = pygame.display.set_mode((800, 600))

    # Заголовок окна игры
    pygame.display.set_caption("Match 3")

    # Основной цикл игры
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                change_colors(board)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Отображение графики
        screen.fill((0, 0, 0))
        for i in range(board_size[0]):
            for j in range(board_size[1]):
                pygame.draw.circle(
                    screen,
                    circle_colors[board[i][j]],
                    (i * 64 - 32, j * 64 - 32),
                    32,
                )

        # Обновление экрана
        pygame.display.flip()


if __name__ == "__main__":
    main()
