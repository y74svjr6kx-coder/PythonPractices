import datetime
import pygame
from clock import MickeyClock, WIDTH, HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    app = MickeyClock()
    running = True
    last_second = None
    timer = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        now = datetime.datetime.now().astimezone()

      second_key = (now.year, now.month, now.day, now.hour, now.minute, now.second)
        if second_key != last_second:
            app.draw(screen, now)
            pygame.display.flip()
            last_second = second_key
        timer.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
