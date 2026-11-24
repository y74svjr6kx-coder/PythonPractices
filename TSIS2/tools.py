from collections import deque
import pygame


def draw_pencil(surface, start, end, color, size):
    pygame.draw.line(surface, color, start, end, size)
    pygame.draw.circle(surface, color, end, max(1, size // 2))


def flood_fill(surface, start, new_color):
    width, height = surface.get_size()
    x, y = start
    if not (0 <= x < width and 0 <= y < height):
        return
    old_color = surface.get_at((x, y))
    replacement = pygame.Color(*new_color)
    if old_color == replacement:
        return
    queue = deque([(x, y)])
    surface.lock()
    try:
        while queue:
            x, y = queue.pop()
            if surface.get_at((x, y)) != old_color:
                continue
            left = x
            while left > 0 and surface.get_at((left - 1, y)) == old_color:
                left -= 1
            right = x
            while right + 1 < width and surface.get_at((right + 1, y)) == old_color:
                right += 1
            for px in range(left, right + 1):
                surface.set_at((px, y), replacement)
            for ny in (y - 1, y + 1):
                if not (0 <= ny < height):
                    continue
                in_segment = False
                for px in range(left, right + 1):
                    matching = surface.get_at((px, ny)) == old_color
                    if matching and not in_segment:
                        queue.append((px, ny))
                    in_segment = matching
    finally:
        surface.unlock()
