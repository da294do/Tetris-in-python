import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Tetris V(1.0)")
clock = pygame.time.Clock()

grid = [[0]*10 for _ in range(20)]

Score = 0

TickEvent = pygame.USEREVENT + 1
pygame.time.set_timer(TickEvent, 500)

Square = pygame.image.load("assets/square.png")
ShrinkedSquare = pygame.transform.scale(Square, (30, 30))


Forms = {
    "Square":  [[5, 10], [6, 10], [5, 9],  [6, 9]],
    "Line":    [[5, 10], [5, 9],  [5, 8],  [5, 7]],
    "L-Shape": [[5, 10], [5, 9],  [5, 8],  [6, 8]],
    "Z-Shape": [[5, 10], [5, 9],  [6, 9],  [6, 8]],
    "T-Shape": [[5, 10], [4, 9],  [5, 9],  [6, 9]],
}

current_form_type = random.choice(list(Forms.keys()))
current_form = [block[:] for block in Forms[current_form_type]]
for block in current_form:
    grid[block[1]][block[0]] = 1


def is_valid_position(form):
    for block in form:
        if not (0 <= block[0] < 10) or not (0 <= block[1] < 20):
            return False
        if block not in current_form and grid[block[1]][block[0]] == 1:
            return False
    return True


def Rotate():
    global current_form

    pivot = current_form[0]

    rotated = []
    for block in current_form:
        rel_x = block[0] - pivot[0]
        rel_y = block[1] - pivot[1]
        new_x = pivot[0] + rel_y
        new_y = pivot[1] - rel_x
        rotated.append([new_x, new_y])

    for x_offset in [0, 1, -1, 2, -2]:
        kicked = [[b[0] + x_offset, b[1]] for b in rotated]
        if is_valid_position(kicked):
            for block in current_form:
                grid[block[1]][block[0]] = 0
            current_form = kicked
            for block in current_form:
                grid[block[1]][block[0]] = 1
            return


def Move(dx, dy):
    global current_form

    new_form = [[b[0] + dx, b[1] + dy] for b in current_form]

    if not is_valid_position(new_form):
        if dy == 1:
            lock_piece_and_spawn_new()
        return

    for block in current_form:
        grid[block[1]][block[0]] = 0
    current_form = new_form
    for block in current_form:
        grid[block[1]][block[0]] = 1


def lock_piece_and_spawn_new():
    global current_form, current_form_type

    ScoreCheck()

    current_form_type = random.choice(list(Forms.keys()))
    current_form = [block[:] for block in Forms[current_form_type]]

    for block in current_form:
        if grid[block[1]][block[0]] == 1:
            print("Game Over")
            pygame.quit()
            sys.exit()

    for block in current_form:
        grid[block[1]][block[0]] = 1


def ScoreCheck():
    global grid, Score
    rows_cleared = 0
    new_grid = []

    for row in grid:
        if all(cell == 1 for cell in row):
            rows_cleared += 1
        else:
            new_grid.append(row)

    for _ in range(rows_cleared):
        new_grid.insert(0, [0] * 10)

    grid[:] = new_grid

    if rows_cleared:
        Score += rows_cleared * 100
        print(f"{Score} SCORE")


running = True
while running:
    clock.tick(60)

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == TickEvent:
            Move(0, 1)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                Move(1, 0)
            elif event.key == pygame.K_DOWN:
                Move(0, 1)
            elif event.key == pygame.K_SPACE:
                Rotate()

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 1:
                screen.blit(ShrinkedSquare, (col * 30, row * 30))

    pygame.display.flip()

pygame.quit()
sys.exit()