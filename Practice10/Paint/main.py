import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
TOOLBAR = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

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

tools = ["Rectangle", "Circle", "Eraser"]
colors = [BLACK, RED, GREEN, BLUE, YELLOW]

tool_buttons = [
    pygame.Rect(10 + i * 110, 10, 100, 40)
    for i in range(len(tools))
]

color_buttons = [
    pygame.Rect(360 + i * 50, 15, 30, 30)
    for i in range(len(colors))
]


def draw_shape(surface, start, end):

    x = min(start[0], end[0])
    y = min(start[1], end[1])

    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])

    if tool == "Rectangle":
        pygame.draw.rect(
            surface, color,
            (x, y, width, height), 3
        )

    elif tool == "Circle":
        radius = int(
            ((end[0] - start[0]) ** 2
             + (end[1] - start[1]) ** 2) ** 0.5
        )

        pygame.draw.circle(
            surface, color, start, radius, 3
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
        screen.blit(text, text.get_rect(center=button.center))

    for i, button in enumerate(color_buttons):

        pygame.draw.rect(screen, colors[i], button)

        if color == colors[i]:
            pygame.draw.rect(screen, WHITE, button, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
