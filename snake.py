# Snake game for BBC MicroBit.
#
# Erik van Zijst <erik.van.zijst@gmail.com>

from microbit import *
import random

def paint(board):
    display.show(Image(":".join(("".join(map(str, row)) for row in board))))

def value(board, x, y):
    return board[y][x]

def set_off(board, x, y):
    board[y][x] = 0

def set_on(board, x, y):
    prev, board[y][x] = board[y][x], 9
    return prev

def place_food(board):
    while True:
        x, y = random.randint(0, 4), random.randint(0, 4)
        if not (board[y][x]):
            board[y][x] = 4
            break

dirs = ((0, -1),    # up
        (1, 0),     # right
        (0, 1),     # down
        (-1, 0))    # left

display.clear()
display.scroll('snake')
sleep(1000)

def game():
    board = [([0] * 5) for _ in range(5)]   # board[y][x]
    snake = [(2, 2), (2, 3)]
    score = 0
    tick = 500
    last = running_time()

    place_food(board)
    paint(board)

    direction = 0
    while True:
        if button_a.was_pressed():
            direction = (direction - 1) % 4
        if button_b.was_pressed():
            direction = (direction + 1) % 4
    
        if running_time() - last > tick:
            score += 1
            # make a move
            head, tail = snake[0], snake[-1]
            
            # new head:
            head = ((head[0] + dirs[direction][0]) % 5, (head[1] + dirs[direction][1]) % 5)
            if head in snake:
                return score
            snake.insert(0, head)
    
            if set_on(board, *head):
                # eat, grow and place new food
                score += 10
                place_food(board)
            else:
                set_off(board, *tail)
                snake = snake[:-1]

            last = running_time()
            paint(board)

display.scroll('score: %d ' % game(), loop=True)
