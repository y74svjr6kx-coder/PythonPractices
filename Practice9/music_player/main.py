import pygame
from player import MusicPlayer

WIDTH, HEIGHT = 760, 400


def fmt(seconds):
    seconds = max(0, int(seconds))
    return f'{seconds // 60:02d}:{seconds % 60:02d}'


def main():
    pygame.init()

    try:
        pygame.mixer.init()
    except pygame.error as exc:
        print(f'Audio device unavailable: {exc}')
        pygame.quit()
        return

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pygame Music Player')

    player = MusicPlayer()

    title_font = pygame.font.SysFont('arial', 35, bold=True)
    font = pygame.font.SysFont('arial', 23)
    small_font = pygame.font.SysFont('arial', 18)

    timer = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_SPACE:
                    player.pause_resume()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next()
                elif event.key == pygame.K_b:
                    player.previous()
            else:
                player.handle_event(event)

        player.update()

        screen.fill((20, 25, 43))

        screen.blit(
            title_font.render('Music Player', True, (255, 255, 255)),
            (35, 28)
        )

        track_name = (
            player.current.name
            if player.current
            else 'No tracks available'
        )

        screen.blit(
            font.render('Track: ' + track_name[:45], True, (180, 225, 255)),
            (35, 108)
        )

        status = (
            'PAUSED' if player.paused
            else 'PLAYING' if player.playing
            else 'STOPPED'
        )

        count = player.index + 1 if player.current else 0

        screen.blit(
            font.render(
                f'{status}  |  {count}/{len(player.playlist)} tracks',
                True,
                (240, 240, 245)
            ),
            (35, 150)
        )

        pygame.draw.rect(
            screen,
            (65, 72, 90),
            (35, 218, 680, 18),
            border_radius=9
        )

        fraction = (
            min(1.0, player.position_seconds / player.duration_seconds)
            if player.duration_seconds else 0
        )

        if fraction > 0:
            pygame.draw.rect(
                screen,
                (80, 205, 155),
                (35, 218, max(1, int(680 * fraction)), 18),
                border_radius=9
            )

        duration = (
            fmt(player.duration_seconds)
            if player.duration_seconds
            else '--:--'
        )

        screen.blit(
            small_font.render(
                f'{fmt(player.position_seconds)} / {duration}',
                True,
                (240, 240, 245)
            ),
            (35, 251)
        )

        screen.blit(
            small_font.render(
                'P Play  SPACE Pause/Resume  S Stop  N Next  B Previous  Q Quit',
                True,
                (255, 215, 125)
            ),
            (35, 310)
        )

        if player.error:
            screen.blit(
                small_font.render(
                    player.error[:72],
                    True,
                    (255, 120, 120)
                ),
                (35, 355)
            )

        pygame.display.flip()
        timer.tick(30)

    player.stop()
    pygame.mixer.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
