import pygame
import datetime

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint TSIS2")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE_ACTIVE = (150, 150, 255)

COLORS = [
    (0, 0, 0), (255, 255, 255), (255, 0, 0),
    (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (255, 165, 0), (128, 0, 128), (0, 255, 255),
    (255, 192, 203)
]

current_color = BLACK
current_tool = "pencil"
brush_size = 2
drawing = False
start_pos = None

text_pos = None
text_input = ""
typing = False

canvas = pygame.Surface((WIDTH, HEIGHT - 100))
canvas.fill(WHITE)
preview = canvas.copy()

font = pygame.font.SysFont(None, 24)
text_font = pygame.font.SysFont(None, 32)

tools = ["pencil", "line", "rect", "circle", "eraser",
         "square", "rtriangle", "etriangle", "rhombus", "fill", "text"]
sizes = [2, 5, 10]


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 100))

    for i, color in enumerate(COLORS):
        rect = pygame.Rect(10 + i * 45, 8, 35, 35)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if color == current_color:
            pygame.draw.rect(screen, BLACK, rect, 4)

    size_labels = ["1:S", "2:M", "3:L"]
    for i, label in enumerate(size_labels):
        rect = pygame.Rect(10 + i * 60, 50, 50, 22)
        color = BLUE_ACTIVE if sizes[i] == brush_size else GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        screen.blit(font.render(label, True, BLACK), (rect.x + 8, rect.y + 4))

    for i, tool in enumerate(tools):
        rect = pygame.Rect(10 + i * 72, 75, 68, 22)
        color = BLUE_ACTIVE if tool == current_tool else GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        screen.blit(font.render(tool, True, BLACK), (rect.x + 3, rect.y + 4))


def flood_fill(surface, x, y, fill_color):
    target_color = surface.get_at((x, y))
    if target_color == fill_color:
        return
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if cx < 0 or cx >= surface.get_width() or cy < 0 or cy >= surface.get_height():
            continue
        if surface.get_at((cx, cy)) != target_color:
            continue
        surface.set_at((cx, cy), fill_color)
        stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])


def draw_shape(surface, tool, start, end, color, size):
    w = end[0] - start[0]
    h = end[1] - start[1]

    if tool == "rect":
        pygame.draw.rect(surface, color, (*start, w, h), size)
    elif tool == "circle":
        cx = (start[0] + end[0]) // 2
        cy = (start[1] + end[1]) // 2
        r = max(abs(w), abs(h)) // 2
        pygame.draw.circle(surface, color, (cx, cy), r, size)
    elif tool == "line":
        pygame.draw.line(surface, color, start, end, size)
    elif tool == "square":
        side = min(abs(w), abs(h))
        pygame.draw.rect(surface, color, (*start, side, side), size)
    elif tool == "rtriangle":
        p1, p2, p3 = start, (start[0], end[1]), end
        pygame.draw.polygon(surface, color, [p1, p2, p3], size)
    elif tool == "etriangle":
        side = abs(w)
        p1 = (start[0] + side // 2, start[1])
        p2 = (start[0], start[1] + side)
        p3 = (start[0] + side, start[1] + side)
        pygame.draw.polygon(surface, color, [p1, p2, p3], size)
    elif tool == "rhombus":
        cx = (start[0] + end[0]) // 2
        cy = (start[1] + end[1]) // 2
        p1 = (cx, start[1])
        p2 = (end[0], cy)
        p3 = (cx, end[1])
        p4 = (start[0], cy)
        pygame.draw.polygon(surface, color, [p1, p2, p3, p4], size)


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = f"canvas_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                pygame.image.save(canvas, filename)
                print(f"Сохранено: {filename}")

            elif event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            elif typing:
                if event.key == pygame.K_RETURN:
                    if text_pos and text_input:
                        text_surface = text_font.render(text_input, True, current_color)
                        canvas.blit(text_surface, text_pos)
                    typing = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if y < 45:
                for i, color in enumerate(COLORS):
                    rect = pygame.Rect(10 + i * 45, 8, 35, 35)
                    if rect.collidepoint(x, y):
                        current_color = color

            elif y < 72:
                for i, size in enumerate(sizes):
                    rect = pygame.Rect(10 + i * 60, 50, 50, 22)
                    if rect.collidepoint(x, y):
                        brush_size = size

            elif y < 100:
                for i, tool in enumerate(tools):
                    rect = pygame.Rect(10 + i * 72, 75, 68, 22)
                    if rect.collidepoint(x, y):
                        current_tool = tool

            else:
                canvas_x, canvas_y = x, y - 100

                if current_tool == "fill":
                    flood_fill(canvas, canvas_x, canvas_y, current_color)

                elif current_tool == "text":
                    text_pos = (canvas_x, canvas_y)
                    typing = True
                    text_input = ""

                else:
                    drawing = True
                    start_pos = (canvas_x, canvas_y)
                    preview = canvas.copy()

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                x, y = event.pos
                end_pos = (x, y - 100)

                if current_tool not in ["pencil", "eraser"]:
                    draw_shape(canvas, current_tool, start_pos, end_pos, current_color, brush_size)

            drawing = False
            start_pos = None

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                x, y = event.pos
                canvas_pos = (x, y - 100)

                if current_tool in ["pencil", "eraser"]:
                    color = WHITE if current_tool == "eraser" else current_color
                    pygame.draw.circle(canvas, color, canvas_pos, brush_size)

                elif current_tool in ["line", "rect", "circle", "square",
                                      "rtriangle", "etriangle", "rhombus"]:
                    preview = canvas.copy()
                    draw_shape(preview, current_tool, start_pos, canvas_pos, current_color, brush_size)

    screen.fill(GRAY)
    draw_toolbar()

    if drawing and current_tool not in ["pencil", "eraser", "fill", "text"]:
        screen.blit(preview, (0, 100))
    else:
        screen.blit(canvas, (0, 100))

    if typing and text_pos:
        text_surface = text_font.render(text_input + "|", True, current_color)
        screen.blit(text_surface, (text_pos[0], text_pos[1] + 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
