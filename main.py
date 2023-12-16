import pygame
import random
import sys
import time
import asyncio

BLOCK_SIZE = 50
BOARD_SIZE = 10
SCREEN_SIZE = BLOCK_SIZE * BOARD_SIZE
SCREEN_COLOR = (0, 0, 0)
SELECT_COLOR = (255, 255, 255)
SELECT_WIDTH = BLOCK_SIZE // 10
INACTIVE_COLOR_COEF = 0.5


# Цвета кружочков
circle_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]


def draw_board(screen, board, pos, selected, active):
    screen.fill(SCREEN_COLOR)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            color = circle_colors[board[i][j]] if not board[i][j] is None else SCREEN_COLOR
            if not active[i][j]:
                color = tuple(int(item * INACTIVE_COLOR_COEF) for item in color)
            pygame.draw.circle(
                screen,
                color,  
                (i * BLOCK_SIZE + BLOCK_SIZE // 2, j * BLOCK_SIZE + BLOCK_SIZE // 2),
                BLOCK_SIZE // 2,
            )

    for p in [pos, selected]:
        if p is None or not active[p[0]][p[1]]:
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


def match3(board, active):
    changed = False
    for i in range(BOARD_SIZE):
        cnt = 1
        for j in range(1, BOARD_SIZE):
            if board[i][j] == board[i][j - 1] and board[i][j] is not None and active[i][j] and active[i][j - 1]:
                cnt += 1
                continue
            if cnt >= 3:
                changed = True
                for k in range(j - cnt, j):
                    board[i][k] = None
            cnt = 1
        if cnt >= 3:
            changed = True
            for k in range(BOARD_SIZE - cnt, BOARD_SIZE):
                board[i][k] = None

    for j in range(BOARD_SIZE):
        cnt = 1
        for i in range(1, BOARD_SIZE):
            if board[i][j] == board[i - 1][j] and board[i][j] is not None and active[i][j] and active[i - 1][j]:
                cnt += 1
                continue
            if cnt >= 3:
                changed = True
                for k in range(i - cnt, i):
                    board[k][j] = None
            cnt = 1
        if cnt >= 3:
            changed = True
            for k in range(BOARD_SIZE - cnt, BOARD_SIZE):
                board[k][j] = None
    return changed


def update_active(board, active):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE - 1, -1, -1):
            active[i][j] = True
            if j < BOARD_SIZE - 1 and active[i][j + 1] == False:
                active[i][j] = False
            if board[i][j] is None:
                active[i][j] = False 


def fall(board, active):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE - 1, 0, -1):
            if not active[i][j]:
                board[i][j], board[i][j - 1] = board[i][j - 1], board[i][j]
        if not active[i][0]:
            board[i][0] = random.randint(0, len(circle_colors) - 1)




async def main():
    # Игровое поле
    board = []
    active = []
    for i in range(BOARD_SIZE):
        board.append([0] * BOARD_SIZE)
        active.append([True] * BOARD_SIZE)

    change_colors(board)

    # Инициализация PyGame
    pygame.init()

    # Создание окна игры
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

    # Заголовок окна игры
    pygame.display.set_caption("Match 3")

    selected = None

    iteration = 0

    # Основной цикл игры
    while True:
        iteration += 1
        mouse_pos = pygame.mouse.get_pos()
        pos = mouse_to_board(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not active[pos[0]][pos[1]]:
                    continue
                if selected is None:
                    selected = pos
                else:
                    if check_swap(pos, selected):
                        board[pos[0]][pos[1]], board[selected[0]][selected[1]] = (
                            board[selected[0]][selected[1]], board[pos[0]][pos[1]]
                        )
                        if not match3(board, active):
                            board[pos[0]][pos[1]], board[selected[0]][selected[1]] = (
                                board[selected[0]][selected[1]], board[pos[0]][pos[1]]
                            )
                    selected = None
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        match3(board, active)
        update_active(board, active)
        if iteration % 10 == 0:
            fall(board, active)
            update_active(board, active)
        draw_board(screen, board, pos, selected, active)
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(main())
