import pygame
from ball import Ball, WIDTH, HEIGHT, STEP


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Moving Red Ball - Arrow Keys')
    ball = Ball()
    timer = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    ball.move(0, -STEP)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, STEP)
                elif event.key == pygame.K_LEFT:
                    ball.move(-STEP, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(STEP, 0)
        screen.fill((255, 255, 255))
        ball.draw(screen)
        pygame.display.flip()
        timer.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
