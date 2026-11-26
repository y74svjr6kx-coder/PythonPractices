import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

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

    if positions:
        return random.choice(positions)

    return None


food = create_food()
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
        score += 1

        if score % 3 == 0:
            level += 1
            speed += 2

        food = create_food()

        if food is None:
            running = False
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
        screen, RED,
        (food[0], food[1], CELL, CELL)
    )

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (25, 25))
    screen.blit(level_text, (WIDTH - 120, 25))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
