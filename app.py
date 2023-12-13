import pygame
import random
import sys

BLOCK_SIZE = 50
BOARD_SIZE = 10
SCREEN_SIZE = BLOCK_SIZE * BOARD_SIZE
SCREEN_COLOR = (0, 0, 0)
SELECT_COLOR = (255, 255, 255)
SELECT_WIDTH = BLOCK_SIZE // 10


# Цвета кружочков
circle_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]


def draw_board(screen, board, pos, selected):
    screen.fill(SCREEN_COLOR)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            pygame.draw.circle(
                screen,
                circle_colors[board[i][j]] if not board[i][j] is None else SCREEN_COLOR, 
                (i * BLOCK_SIZE + BLOCK_SIZE // 2, j * BLOCK_SIZE + BLOCK_SIZE // 2),
                BLOCK_SIZE // 2,
            )

    for p in [pos, selected]:
        if p is None:
            continue
        pygame.draw.circle(
            screen,
            SELECT_COLOR,
            (p[0] * BLOCK_SIZE + BLOCK_SIZE // 2, p[1] * BLOCK_SIZE + BLOCK_SIZE // 2),
            BLOCK_SIZE // 2,
            SELECT_WIDTH
        )
    # Обновление экрана
    pygame.display.flip()


def check_swap(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
        

def change_colors(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            board[i][j] = random.randint(0, len(circle_colors) - 1)


def mouse_to_board(mouse_pos):
    x = mouse_pos[0] // BLOCK_SIZE
    y = mouse_pos[1] // BLOCK_SIZE
    return x, y


def match3(board):
    for i in range(1, BOARD_SIZE):
        cnt = 1
        for j in range(1, BOARD_SIZE):
            if board[i][j] == board[i][j - 1] and board[i][j] is not None:
                cnt += 1
                continue
            if cnt >= 3:
                for k in range(j - cnt, j):
                    board[i][k] = None
            cnt = 1
        if cnt >= 3:
            for k in range(BOARD_SIZE - cnt, BOARD_SIZE):
                board[i][k] = None

    for j in range(1, BOARD_SIZE):
        cnt = 1
        for i in range(1, BOARD_SIZE):
            if board[i][j] == board[i - 1][j] and board[i][j] is not None:
                cnt += 1
                continue
            if cnt >= 3:
                for k in range(i - cnt, i):
                    board[k][j] = None
            cnt = 1
        if cnt >= 3:
            for k in range(BOARD_SIZE - cnt, BOARD_SIZE):
                board[k][j] = None


def main():
    # Игровое поле
    board = []
    for i in range(BOARD_SIZE):
        board.append([0] * BOARD_SIZE)

    change_colors(board)

    # Инициализация PyGame
    pygame.init()

    # Создание окна игры
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

    # Заголовок окна игры
    pygame.display.set_caption("Match 3")

    selected = None

    # Основной цикл игры
    while True:
        mouse_pos = pygame.mouse.get_pos()
        pos = mouse_to_board(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selected is None:
                    selected = pos
                else:
                    if check_swap(pos, selected):
                        board[pos[0]][pos[1]], board[selected[0]][selected[1]] = (
                            board[selected[0]][selected[1]], board[pos[0]][pos[1]]
                        )  
                    selected = None
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        match3(board)
        draw_board(screen, board, pos, selected)

if __name__ == "__main__":
    main()
