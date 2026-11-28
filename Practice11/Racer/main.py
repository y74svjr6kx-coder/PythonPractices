import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)

WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
SILVER = (192, 192, 192)
ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)

player = pygame.Rect(175, 480, 50, 90)
enemy = pygame.Rect(random.randint(60, 290), -90, 50, 90)

coin_colors = {
    1: YELLOW,
    2: SILVER,
    3: ORANGE
}


def create_coin():
    weight = random.choice([1, 2, 3])
    coin = pygame.Rect(random.randint(60, 320), -30, 20, 20)
    return coin, weight


coin, weight = create_coin()

score = 0
enemy_speed = 5
coin_speed = 5
road_offset = 0
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x = max(60, player.x - 5)

    if keys[pygame.K_RIGHT]:
        player.x = min(290, player.x + 5)

    enemy.y += enemy_speed

    if enemy.top > HEIGHT:
        enemy.y = -90
        enemy.x = random.randint(60, 290)

    coin.y += coin_speed

    if coin.top > HEIGHT:
        coin, weight = create_coin()

    if player.colliderect(coin):
        score += weight
        enemy_speed = 5 + score // 5
        coin, weight = create_coin()

    if player.colliderect(enemy):
        running = False

    screen.fill(GREEN)

    pygame.draw.rect(screen, GRAY, (50, 0, 300, HEIGHT))

    pygame.draw.line(screen, WHITE, (55, 0), (55, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (345, 0), (345, HEIGHT), 4)

    road_offset = (road_offset + 5) % 100

    for y in range(-100, HEIGHT, 100):
        pygame.draw.rect(
            screen, WHITE,
            (195, y + road_offset, 10, 50)
        )

    pygame.draw.rect(screen, BLUE, player, border_radius=8)
    pygame.draw.rect(screen, RED, enemy, border_radius=8)

    pygame.draw.rect(
        screen, WHITE,
        (player.x + 8, player.y + 15, 34, 20)
    )

    pygame.draw.rect(
        screen, WHITE,
        (enemy.x + 8, enemy.y + 15, 34, 20)
    )

    pygame.draw.circle(
        screen, coin_colors[weight], coin.center, 10
    )

    coin_text = small_font.render(str(weight), True, BLACK)

    screen.blit(
        coin_text,
        coin_text.get_rect(center=coin.center)
    )

    score_text = font.render(f"Coins: {score}", True, WHITE)
    speed_text = font.render(f"Speed: {enemy_speed}", True, WHITE)

    screen.blit(
        score_text,
        (WIDTH - score_text.get_width() - 10, 10)
    )

    screen.blit(speed_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
