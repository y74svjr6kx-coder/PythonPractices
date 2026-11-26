import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)

# Create player and enemy cars
player = pygame.Rect(175, 480, 50, 90)
enemy = pygame.Rect(random.randint(60, 290), -90, 50, 90)

# Create a coin at a random position
def create_coin():
    return pygame.Rect(random.randint(60, 320), -30, 20, 20)


coin = create_coin()
score = 0
speed = 5
road_offset = 0
running = True

while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > 60:
        player.x -= 5

    if keys[pygame.K_RIGHT] and player.right < 340:
        player.x += 5

    # Move the enemy
    enemy.y += speed

    if enemy.top > HEIGHT:
        enemy.y = -90
        enemy.x = random.randint(60, 290)

    # Move the coin
    coin.y += speed

    if coin.top > HEIGHT:
        coin = create_coin()

    # Check coin collection
    if player.colliderect(coin):
        score += 1
        coin = create_coin()

    # Check car collision
    if player.colliderect(enemy):
        running = False

    # Draw the road
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (50, 0, 300, HEIGHT))

    pygame.draw.line(screen, WHITE, (55, 0), (55, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (345, 0), (345, HEIGHT), 4)

    # Animate road markings
    road_offset = (road_offset + speed) % 100

    for y in range(-100, HEIGHT, 100):
        pygame.draw.rect(
            screen, WHITE,
            (195, y + road_offset, 10, 50)
        )

    # Draw cars
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

    # Draw the coin
    pygame.draw.circle(screen, YELLOW, coin.center, 10)

    # Display collected coins
    text = font.render(f"Coins: {score}", True, WHITE)
    screen.blit(text, (WIDTH - text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
