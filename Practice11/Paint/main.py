import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR = 110

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR))
canvas.fill(WHITE)

color = BLACK
tool = "Rectangle"

drawing = False
start = None
previous = None

tools = [
    "Rectangle",
    "Circle",
    "Eraser",
    "Square",
    "Right Triangle",
    "Equilateral Triangle",
    "Rhombus"
]

colors = [BLACK, RED, GREEN, BLUE, YELLOW]

tool_buttons = [
    pygame.Rect(10 + i * 140, 10, 130, 40)
    for i in range(len(tools))
]

color_buttons = [
    pygame.Rect(10 + i * 50, 65, 30, 30)
    for i in range(len(colors))
]


def draw_shape(surface, start, end):

    x1, y1 = start
    x2, y2 = end

    x = min(x1, x2)
    y = min(y1, y2)

    width = abs(x2 - x1)
    height = abs(y2 - y1)

    if tool == "Rectangle":

        pygame.draw.rect(
            surface, color,
            (x, y, width, height), 3
        )

    elif tool == "Circle":

        radius = int(
            math.hypot(x2 - x1, y2 - y1)
        )

        pygame.draw.circle(
            surface, color, start, radius, 3
        )

    elif tool == "Square":

        size = min(width, height)

        square_x = x1 if x2 >= x1 else x1 - size
        square_y = y1 if y2 >= y1 else y1 - size

        pygame.draw.rect(
            surface, color,
            (square_x, square_y, size, size), 3
        )

    elif tool == "Right Triangle":

        points = [
            (x1, y1),
            (x1, y2),
            (x2, y2)
        ]

        pygame.draw.polygon(
            surface, color, points, 3
        )

    elif tool == "Equilateral Triangle":

        side = width
        triangle_height = side * math.sqrt(3) / 2

        base_y = y1 + triangle_height if y2 >= y1 else y1 - triangle_height

        points = [
            (x + side / 2, y1),
            (x, base_y),
            (x + side, base_y)
        ]

        pygame.draw.polygon(
            surface, color, points, 3
        )

    elif tool == "Rhombus":

        points = [
            (x + width / 2, y),
            (x + width, y + height / 2),
            (x + width / 2, y + height),
            (x, y + height / 2)
        ]

        pygame.draw.polygon(
            surface, color, points, 3
        )


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                x, y = event.pos

                if y < TOOLBAR:

                    for i, button in enumerate(tool_buttons):
                        if button.collidepoint(event.pos):
                            tool = tools[i]

                    for i, button in enumerate(color_buttons):
                        if button.collidepoint(event.pos):
                            color = colors[i]

                else:

                    drawing = True
                    start = (x, y - TOOLBAR)
                    previous = start

                    if tool == "Eraser":
                        pygame.draw.circle(
                            canvas, WHITE, start, 10
                        )

        elif event.type == pygame.MOUSEMOTION:

            if drawing and tool == "Eraser":

                x, y = event.pos
                current = (x, y - TOOLBAR)

                pygame.draw.line(
                    canvas, WHITE, previous, current, 20
                )

                pygame.draw.circle(
                    canvas, WHITE, current, 10
                )

                previous = current

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and drawing:

                x, y = event.pos
                end = (x, y - TOOLBAR)

                if tool != "Eraser":
                    draw_shape(canvas, start, end)

                drawing = False

    screen.fill(GRAY)
    screen.blit(canvas, (0, TOOLBAR))

    if drawing and tool != "Eraser":

        preview = canvas.copy()

        x, y = pygame.mouse.get_pos()

        draw_shape(
            preview, start, (x, y - TOOLBAR)
        )

        screen.blit(preview, (0, TOOLBAR))

    for i, button in enumerate(tool_buttons):

        pygame.draw.rect(screen, WHITE, button)

        if tool == tools[i]:
            pygame.draw.rect(screen, BLUE, button, 3)
        else:
            pygame.draw.rect(screen, BLACK, button, 1)

        text = font.render(tools[i], True, BLACK)

        screen.blit(
            text, text.get_rect(center=button.center)
        )

    for i, button in enumerate(color_buttons):

        pygame.draw.rect(screen, colors[i], button)

        if color == colors[i]:
            pygame.draw.rect(screen, WHITE, button, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
