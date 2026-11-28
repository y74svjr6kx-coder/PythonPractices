import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20
FOOD_TIME = 5000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 215, 0)
PURPLE = (160, 32, 240)

food_colors = {
    1: RED,
    2: YELLOW,
    3: PURPLE
}

snake = [(300, 200), (280, 200), (260, 200)]
direction = (CELL, 0)

score = 0
level = 1
speed = 8


def create_food():
    positions = []

    for x in range(CELL, WIDTH - CELL, CELL):
        for y in range(CELL, HEIGHT - CELL, CELL):
            if (x, y) not in snake:
                positions.append((x, y))

    if not positions:
        return None, 0, pygame.time.get_ticks()

    position = random.choice(positions)
    weight = random.choice([1, 2, 3])
    spawn_time = pygame.time.get_ticks()

    return position, weight, spawn_time


food, weight, spawn_time = create_food()

running = True

while running:

    next_direction = direction

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and direction != (0, CELL):
                next_direction = (0, -CELL)

            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                next_direction = (0, CELL)

            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                next_direction = (-CELL, 0)

            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                next_direction = (CELL, 0)

    if not running:
        break

    direction = next_direction

    current_time = pygame.time.get_ticks()

    if current_time - spawn_time >= FOOD_TIME:
        food, weight, spawn_time = create_food()

    if food is None:
        break

    head = (
        snake[0][0] + direction[0],
        snake[0][1] + direction[1]
    )

    if (
        head[0] < CELL
        or head[0] >= WIDTH - CELL
        or head[1] < CELL
        or head[1] >= HEIGHT - CELL
    ):
        running = False
        break

    body = snake if head == food else snake[:-1]

    if head in body:
        running = False
        break

    snake.insert(0, head)

    if head == food:

        score += weight

        level = 1 + score // 3
        speed = 8 + (level - 1) * 2

        food, weight, spawn_time = create_food()

        if food is None:
            break

    else:
        snake.pop()

    screen.fill(BLACK)

    pygame.draw.rect(
        screen, GRAY,
        (0, 0, WIDTH, HEIGHT),
        CELL
    )

    for x, y in snake:
        pygame.draw.rect(
            screen, GREEN,
            (x, y, CELL - 1, CELL - 1)
        )

    pygame.draw.rect(
        screen, food_colors[weight],
        (food[0], food[1], CELL, CELL)
    )

    remaining_time = max(
        0,
        (FOOD_TIME - (pygame.time.get_ticks() - spawn_time)) / 1000
    )

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    timer_text = font.render(f"Time: {remaining_time:.1f}", True, WHITE)

    screen.blit(score_text, (25, 25))
    screen.blit(level_text, (250, 25))
    screen.blit(timer_text, (450, 25))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
