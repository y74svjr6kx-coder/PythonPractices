import datetime
import math
import pygame
from zoneinfo import ZoneInfo

WIDTH, HEIGHT = 720, 650
CENTER = (360, 325)
ALMATY = ZoneInfo("Asia/Almaty")


def draw_hand(screen, angle, length, color, width):
    rad = math.radians(angle - 90)

    end_x = CENTER[0] + math.cos(rad) * length
    end_y = CENTER[1] + math.sin(rad) * length

    pygame.draw.line(
        screen,
        (0, 0, 0),
        CENTER,
        (end_x, end_y),
        width + 6
    )

    pygame.draw.line(
        screen,
        color,
        CENTER,
        (end_x, end_y),
        width
    )

    pygame.draw.circle(
        screen,
        color,
        (int(end_x), int(end_y)),
        width + 8
    )

    pygame.draw.circle(
        screen,
        (0, 0, 0),
        (int(end_x), int(end_y)),
        width + 8,
        3
    )


class MickeyClock:
    def __init__(self):
        self.title_font = pygame.font.SysFont(
            "arial", 36, bold=True
        )

        self.time_font = pygame.font.SysFont(
            "arial", 42, bold=True
        )

        self.label_font = pygame.font.SysFont(
            "arial", 20
        )

    def draw(self, screen, now=None):
        if now is None:
            now = datetime.datetime.now(ALMATY)

        screen.fill((245, 248, 255))

        pygame.draw.circle(
            screen, (30, 35, 55), CENTER, 247
        )

        pygame.draw.circle(
            screen, (255, 255, 255), CENTER, 237
        )

        for tick in range(60):
            angle = math.radians(tick * 6 - 90)

            r1 = 211 if tick % 5 == 0 else 223

            x1 = CENTER[0] + math.cos(angle) * r1
            y1 = CENTER[1] + math.sin(angle) * r1

            x2 = CENTER[0] + math.cos(angle) * 231
            y2 = CENTER[1] + math.sin(angle) * 231

            pygame.draw.line(
                screen,
                (30, 35, 55),
                (x1, y1),
                (x2, y2),
                4 if tick % 5 == 0 else 2
            )

        pygame.draw.circle(
            screen,
            (30, 35, 55),
            (CENTER[0] - 115, CENTER[1] - 185),
            66
        )

        pygame.draw.circle(
            screen,
            (30, 35, 55),
            (CENTER[0] + 115, CENTER[1] - 185),
            66
        )

        pygame.draw.circle(
            screen,
            (255, 228, 194),
            CENTER,
            118
        )

        for x in (-39, 39):
            pygame.draw.ellipse(
                screen,
                (255, 255, 255),
                (CENTER[0] + x - 19,
                 CENTER[1] - 77, 38, 66)
            )

            pygame.draw.ellipse(
                screen,
                (20, 20, 25),
                (CENTER[0] + x - 7,
                 CENTER[1] - 41, 14, 29)
            )

        pygame.draw.ellipse(
            screen,
            (22, 22, 28),
            (CENTER[0] - 35,
             CENTER[1] + 18, 70, 40)
        )

        pygame.draw.arc(
            screen,
            (25, 25, 30),
            (CENTER[0] - 69,
             CENTER[1] - 2, 138, 112),
            3.3, 6.1, 4
        )

        minute_angle = (
            now.minute + now.second / 60
        ) * 6

        second_angle = now.second * 6

        draw_hand(
            screen,
            minute_angle,
            165,
            (255, 255, 255),
            12
        )

        draw_hand(
            screen,
            second_angle,
            195,
            (240, 60, 60),
            8
        )

        pygame.draw.circle(
            screen,
            (25, 25, 30),
            CENTER,
            13
        )

        title = self.title_font.render(
            "Mickey's Clock",
            True,
            (25, 30, 45)
        )

        screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, 35))
        )

        value = self.time_font.render(
            now.strftime("%H:%M:%S"),
            True,
            (25, 30, 45)
        )

        screen.blit(
            value,
            value.get_rect(center=(WIDTH // 2, 602))
        )

        legend = self.label_font.render(
            "Almaty Time | White: Minutes | Red: Seconds",
            True,
            (55, 60, 75)
        )

        screen.blit(
            legend,
            legend.get_rect(center=(WIDTH // 2, 638))
        )