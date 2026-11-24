import pygame

WIDTH, HEIGHT = 640, 480
RADIUS = 25
STEP = 20


class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if RADIUS <= new_x <= WIDTH - RADIUS and RADIUS <= new_y <= HEIGHT - RADIUS:
            self.x, self.y = new_x, new_y

    def draw(self, screen):
        pygame.draw.circle(screen, (230, 35, 45), (self.x, self.y), RADIUS)
