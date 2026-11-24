from datetime import datetime
from pathlib import Path
import pygame

from tools import draw_pencil, flood_fill

pygame.init()
WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TSIS 2 - Paint')
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
small_font = pygame.font.SysFont('arial', 16)
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

COLORS = [(0, 0, 0), (230, 60, 60), (35, 140, 65), (45, 100, 230), (245, 175, 40), (155, 65, 190)]
TOOL_BUTTONS = {'pencil': pygame.Rect(12, 10, 105, 35),
                'line': pygame.Rect(125, 10, 105, 35),
                'fill': pygame.Rect(238, 10, 105, 35),
                'text': pygame.Rect(351, 10, 105, 35)}
SIZE_BUTTONS = {2: pygame.Rect(490, 10, 55, 35),
                5: pygame.Rect(550, 10, 55, 35),
                10: pygame.Rect(610, 10, 65, 35)}
COLOR_BUTTONS = [(pygame.Rect(12 + i * 42, 54, 32, 26), color) for i, color in enumerate(COLORS)]

active_tool = 'pencil'
active_color = COLORS[0]
brush_size = 5
drawing = False
start_pos = None
last_pos = None
text_pos = None
text_value = ''
status = 'Ready'


def canvas_pos(mouse_pos):
    x, y = mouse_pos
    if 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT:
        return (x, y - TOOLBAR_HEIGHT)
    return None


def finish_text():
    global text_pos, text_value
    if text_pos is not None and text_value:
        rendered = font.render(text_value, True, active_color)
        canvas.blit(rendered, text_pos)
    text_pos = None
    text_value = ''


def save_canvas():
    global status
    folder = Path(__file__).resolve().parent / 'saves'
    folder.mkdir(exist_ok=True)
    filename = folder / f'painting_{datetime.now():%Y%m%d_%H%M%S_%f}.png'
    pygame.image.save(canvas, str(filename))
    status = f'Saved: {filename.name}'


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                save_canvas()
            elif text_pos is not None:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    finish_text()
                elif event.key == pygame.K_ESCAPE:
                    text_pos = None
                    text_value = ''
                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]
                elif event.unicode and event.unicode.isprintable() and not (event.mod & (pygame.KMOD_CTRL | pygame.KMOD_ALT)):
                    text_value += event.unicode
            elif event.key in (pygame.K_1, pygame.K_KP1):
                brush_size = 2
            elif event.key in (pygame.K_2, pygame.K_KP2):
                brush_size = 5
            elif event.key in (pygame.K_3, pygame.K_KP3):
                brush_size = 10

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = event.pos
            selected = False
            if mouse[1] < TOOLBAR_HEIGHT:
                for tool, rect in TOOL_BUTTONS.items():
                    if rect.collidepoint(mouse):
                        active_tool = tool
                        selected = True
                        break
                for size, rect in SIZE_BUTTONS.items():
                    if rect.collidepoint(mouse):
                        brush_size = size
                        selected = True
                        break
                for rect, color in COLOR_BUTTONS:
                    if rect.collidepoint(mouse):
                        active_color = color
                        selected = True
                        break
                if selected and text_pos is not None:
                    # Switching tools or colors cancels unfinished text.
                    text_pos = None
                    text_value = ''
            else:
                point = canvas_pos(mouse)
                if point is not None:
                    if active_tool == 'fill':
                        flood_fill(canvas, point, active_color)
                    elif active_tool == 'text':
                        text_pos = point
                        text_value = ''
                    else:
                        drawing = True
                        start_pos = point
                        last_pos = point
                        if active_tool == 'pencil':
                            pygame.draw.circle(canvas, active_color, point, max(1, brush_size // 2))

        elif event.type == pygame.MOUSEMOTION and drawing:
            point = canvas_pos(event.pos)
            if active_tool == 'pencil' and point is not None and last_pos is not None:
                draw_pencil(canvas, last_pos, point, active_color, brush_size)
                last_pos = point

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            point = canvas_pos(event.pos)
            if active_tool == 'line' and start_pos is not None and point is not None:
                pygame.draw.line(canvas, active_color, start_pos, point, brush_size)
            elif active_tool == 'pencil' and point is not None and last_pos is not None:
                draw_pencil(canvas, last_pos, point, active_color, brush_size)
            drawing = False
            start_pos = None
            last_pos = None

    screen.fill((228, 232, 238))
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Live preview is displayed on the screen only; the canvas stays unchanged.
    if drawing and active_tool == 'line' and start_pos is not None:
        point = canvas_pos(pygame.mouse.get_pos())
        if point is not None:
            pygame.draw.line(screen, active_color,
                             (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT),
                             (point[0], point[1] + TOOLBAR_HEIGHT), brush_size)

    if text_pos is not None:
        preview = font.render(text_value, True, active_color)
        x, y = text_pos
        screen.blit(preview, (x, y + TOOLBAR_HEIGHT))
        cursor_x = x + preview.get_width()
        pygame.draw.line(screen, active_color, (cursor_x, y + TOOLBAR_HEIGHT),
                         (cursor_x, y + TOOLBAR_HEIGHT + font.get_height()), 2)

    for tool, rect in TOOL_BUTTONS.items():
        pygame.draw.rect(screen, (175, 205, 245) if tool == active_tool else (250, 250, 250), rect, border_radius=5)
        pygame.draw.rect(screen, (80, 95, 115), rect, 2, border_radius=5)
        label = small_font.render(tool.capitalize(), True, (20, 25, 30))
        screen.blit(label, label.get_rect(center=rect.center))

    for size, rect in SIZE_BUTTONS.items():
        pygame.draw.rect(screen, (175, 205, 245) if size == brush_size else (250, 250, 250), rect, border_radius=5)
        pygame.draw.rect(screen, (80, 95, 115), rect, 2, border_radius=5)
        label = small_font.render(str(size), True, (20, 25, 30))
        screen.blit(label, label.get_rect(center=rect.center))

    for rect, color in COLOR_BUTTONS:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (30, 30, 30) if color == active_color else (150, 150, 150), rect, 3 if color == active_color else 1)

    help_text = small_font.render('1 / 2 / 3 = brush size     Ctrl+S = save PNG     Text: Enter = confirm, Esc = cancel', True, (35, 35, 35))
    screen.blit(help_text, (300, 57))
    status_text = small_font.render(status, True, (35, 35, 35))
    screen.blit(status_text, (700, 17))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
