import pygame
import random
import json
from db import create_tables, save_result, get_leaderboard, get_personal_best

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake TSIS3")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
DARK_RED = (100, 0, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BLUE = (50, 100, 200)
GREEN = (50, 200, 50)
DARK_GREEN = (30, 150, 30)
PURPLE = (150, 0, 200)
LIGHT_BLUE = (100, 180, 255)

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 30)
tiny_font = pygame.font.SysFont(None, 24)


def load_settings():
    with open("settings.json", "r") as f:
        return json.load(f)


def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)


settings = load_settings()
create_tables()

screen_state = "menu"
username = ""
username_input = ""
personal_best = 0


def random_pos(snake, obstacles=[]):
    while True:
        x = random.randint(0, WIDTH // CELL - 1) * CELL
        y = random.randint(0, HEIGHT // CELL - 1) * CELL
        if (x, y) not in snake and (x, y) not in obstacles:
            return (x, y)


def new_food(snake, obstacles=[]):
    pos = random_pos(snake, obstacles)
    weight = random.choices([1, 3, 5], weights=[60, 30, 10])[0]
    return {"pos": pos, "weight": weight, "born": pygame.time.get_ticks()}


def new_poison(snake, obstacles=[]):
    pos = random_pos(snake, obstacles)
    return {"pos": pos, "born": pygame.time.get_ticks()}


def new_powerup(snake, obstacles=[]):
    pos = random_pos(snake, obstacles)
    kind = random.choice(["speed", "slow", "shield"])
    return {"pos": pos, "kind": kind, "born": pygame.time.get_ticks()}


def new_obstacles(snake, level):
    count = level * 2
    obstacles = []
    for _ in range(count):
        pos = random_pos(snake, obstacles)
        obstacles.append(pos)
    return obstacles


def reset_game():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (CELL, 0)
    food = new_food(snake)
    poison = new_poison(snake)
    powerup = None
    obstacles = []
    score = 0
    level = 1
    speed = 8
    shield = False
    active_effect = None
    effect_end = 0
    return snake, direction, food, poison, powerup, obstacles, score, level, speed, shield, active_effect, effect_end


snake, direction, food, poison, powerup, obstacles, score, level, speed, shield, active_effect, effect_end = reset_game()
move_timer = 0
final_score = 0
final_level = 1
powerup_spawn_timer = 0
FOOD_LIFETIME = 5000
POWERUP_LIFETIME = 8000


def draw_button(text, x, y, w, h, color=GRAY, text_color=WHITE):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = small_font.render(text, True, text_color)
    screen.blit(label, (x + w // 2 - label.get_width() // 2, y + h // 2 - label.get_height() // 2))
    return rect


def draw_menu():
    screen.fill(BLACK)
    title = font.render("SNAKE", True, GREEN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    input_label = small_font.render("Введи имя:", True, WHITE)
    screen.blit(input_label, (WIDTH // 2 - input_label.get_width() // 2, 180))

    input_box = pygame.Rect(WIDTH // 2 - 100, 215, 200, 35)
    pygame.draw.rect(screen, WHITE, input_box, 2)
    name_text = small_font.render(username_input, True, WHITE)
    screen.blit(name_text, (input_box.x + 5, input_box.y + 7))

    play_btn = draw_button("Play", WIDTH // 2 - 80, 280, 160, 45, BLUE)
    lb_btn = draw_button("Leaderboard", WIDTH // 2 - 80, 340, 160, 45, DARK_GRAY)
    set_btn = draw_button("Settings", WIDTH // 2 - 80, 400, 160, 45, DARK_GRAY)
    quit_btn = draw_button("Quit", WIDTH // 2 - 80, 460, 160, 45, RED)

    return play_btn, lb_btn, set_btn, quit_btn


def draw_game():
    screen.fill(BLACK)

    if settings["grid"]:
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))

    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, (*obs, CELL, CELL))

    now = pygame.time.get_ticks()

    if poison and now - poison["born"] < FOOD_LIFETIME:
        pygame.draw.rect(screen, DARK_RED, (*poison["pos"], CELL, CELL), border_radius=5)
        p_label = tiny_font.render("P", True, WHITE)
        screen.blit(p_label, (poison["pos"][0] + 5, poison["pos"][1] + 3))

    time_left = FOOD_LIFETIME - (now - food["born"])
    food_color = RED if food["weight"] == 1 else (ORANGE if food["weight"] == 3 else CYAN)
    if time_left < 2000 and (now // 300) % 2 == 0:
        food_color = WHITE
    pygame.draw.rect(screen, food_color, (*food["pos"], CELL, CELL), border_radius=5)
    w_label = tiny_font.render(str(food["weight"]), True, BLACK)
    screen.blit(w_label, (food["pos"][0] + 5, food["pos"][1] + 3))

    if powerup and now - powerup["born"] < POWERUP_LIFETIME:
        pu_color = YELLOW if powerup["kind"] == "speed" else (LIGHT_BLUE if powerup["kind"] == "slow" else PURPLE)
        pygame.draw.rect(screen, pu_color, (*powerup["pos"], CELL, CELL), border_radius=5)
        pu_label = tiny_font.render(powerup["kind"][0].upper(), True, BLACK)
        screen.blit(pu_label, (powerup["pos"][0] + 5, powerup["pos"][1] + 3))

    snake_color = tuple(settings["snake_color"])
    dark_color = tuple(max(0, c - 50) for c in snake_color)
    for i, segment in enumerate(snake):
        color = snake_color if i == 0 else dark_color
        pygame.draw.rect(screen, color, (*segment, CELL, CELL), border_radius=4)

    if shield:
        pygame.draw.rect(screen, PURPLE, (*snake[0], CELL, CELL), 3)

    score_text = small_font.render(f"Score: {score}", True, WHITE)
    level_text = small_font.render(f"Level: {level}", True, YELLOW)
    best_text = small_font.render(f"Best: {personal_best}", True, CYAN)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))
    screen.blit(best_text, (WIDTH - best_text.get_width() - 10, 10))

    if active_effect:
        remaining = max(0, (effect_end - now) // 1000)
        effect_text = tiny_font.render(f"{active_effect}: {remaining}s", True, YELLOW)
        screen.blit(effect_text, (10, 35))


def draw_gameover():
    screen.fill(BLACK)
    over = font.render("GAME OVER", True, RED)
    screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 100))

    score_text = small_font.render(f"Score: {final_score}", True, WHITE)
    level_text = small_font.render(f"Level: {final_level}", True, YELLOW)
    best_text = small_font.render(f"Personal Best: {personal_best}", True, CYAN)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 200))
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 240))
    screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, 280))

    retry_btn = draw_button("Retry", WIDTH // 2 - 80, 360, 160, 45, BLUE)
    menu_btn = draw_button("Main Menu", WIDTH // 2 - 80, 420, 160, 45, DARK_GRAY)
    return retry_btn, menu_btn


def draw_leaderboard():
    screen.fill(BLACK)
    title = font.render("TOP 10", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    rows = get_leaderboard()
    for i, row in enumerate(rows):
        text = small_font.render(f"{i+1}. {row[0]} — {row[1]} (lvl {row[2]})", True, WHITE)
        screen.blit(text, (30, 110 + i * 35))

    back_btn = draw_button("Back", WIDTH // 2 - 80, 520, 160, 45, DARK_GRAY)
    return back_btn


def draw_settings():
    screen.fill(BLACK)
    title = font.render("Settings", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    grid_color = BLUE if settings["grid"] else DARK_GRAY
    grid_btn = draw_button(f"Grid: {'ON' if settings['grid'] else 'OFF'}", WIDTH // 2 - 80, 150, 160, 45, grid_color)

    colors = {"Green": [50, 200, 50], "Blue": [50, 100, 200], "Red": [220, 50, 50]}
    color_btns = {}
    for i, (name, color) in enumerate(colors.items()):
        btn = draw_button(name, WIDTH // 2 - 80, 220 + i * 60, 160, 45, tuple(color))
        color_btns[name] = (btn, color)

    save_btn = draw_button("Save & Back", WIDTH // 2 - 80, 480, 160, 45, GREEN)
    return grid_btn, color_btns, save_btn


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    move_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if screen_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username_input = username_input[:-1]
                elif event.key != pygame.K_RETURN:
                    username_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                play_btn, lb_btn, set_btn, quit_btn = draw_menu()
                if play_btn.collidepoint(event.pos) and username_input.strip():
                    username = username_input.strip()
                    personal_best = get_personal_best(username)
                    snake, direction, food, poison, powerup, obstacles, score, level, speed, shield, active_effect, effect_end = reset_game()
                    move_timer = 0
                    screen_state = "game"
                elif lb_btn.collidepoint(event.pos):
                    screen_state = "leaderboard"
                elif set_btn.collidepoint(event.pos):
                    screen_state = "settings"
                elif quit_btn.collidepoint(event.pos):
                    running = False

        elif screen_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                    direction = (CELL, 0)

        elif screen_state == "gameover":
            if event.type == pygame.MOUSEBUTTONDOWN:
                retry_btn, menu_btn = draw_gameover()
                if retry_btn.collidepoint(event.pos):
                    snake, direction, food, poison, powerup, obstacles, score, level, speed, shield, active_effect, effect_end = reset_game()
                    move_timer = 0
                    screen_state = "game"
                elif menu_btn.collidepoint(event.pos):
                    screen_state = "menu"

        elif screen_state == "leaderboard":
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_btn = draw_leaderboard()
                if back_btn.collidepoint(event.pos):
                    screen_state = "menu"

        elif screen_state == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN:
                grid_btn, color_btns, save_btn = draw_settings()
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]
                for name, (btn, color) in color_btns.items():
                    if btn.collidepoint(event.pos):
                        settings["snake_color"] = color
                if save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    screen_state = "menu"

    if screen_state == "game":
        now = pygame.time.get_ticks()

        if now - food["born"] > FOOD_LIFETIME:
            food = new_food(snake, obstacles)

        if poison and now - poison["born"] > FOOD_LIFETIME:
            poison = new_poison(snake, obstacles)

        if powerup and now - powerup["born"] > POWERUP_LIFETIME:
            powerup = None

        if active_effect and now > effect_end:
            if active_effect == "speed":
                speed = max(8, speed - 4)
            elif active_effect == "slow":
                speed = min(20, speed + 4)
            active_effect = None

        powerup_spawn_timer += 1
        if powerup_spawn_timer > 300 and not powerup:
            powerup = new_powerup(snake, obstacles)
            powerup_spawn_timer = 0

        if move_timer >= 60 // speed:
            move_timer = 0
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            hit_wall = head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT
            hit_self = head in snake
            hit_obs = head in obstacles

            if (hit_wall or hit_self or hit_obs):
                if shield:
                    shield = False
                    active_effect = None
                else:
                    final_score = score
                    final_level = level
                    save_result(username, score, level)
                    personal_best = get_personal_best(username)
                    screen_state = "gameover"
            else:
                snake.insert(0, head)

                if head == food["pos"]:
                    score += food["weight"]
                    food = new_food(snake, obstacles)
                    if score % 5 == 0:
                        level += 1
                        speed += 1
                        if level >= 3:
                            obstacles = new_obstacles(snake, level)

                elif poison and head == poison["pos"]:
                    if len(snake) > 3:
                        snake = snake[:-2]
                        snake.pop()
                    else:
                        final_score = score
                        final_level = level
                        save_result(username, score, level)
                        personal_best = get_personal_best(username)
                        screen_state = "gameover"
                    poison = new_poison(snake, obstacles)

                elif powerup and head == powerup["pos"]:
                    if powerup["kind"] == "speed":
                        speed += 4
                        active_effect = "speed"
                        effect_end = now + 5000
                    elif powerup["kind"] == "slow":
                        speed = max(4, speed - 4)
                        active_effect = "slow"
                        effect_end = now + 5000
                    elif powerup["kind"] == "shield":
                        shield = True
                        active_effect = "shield"
                        effect_end = now + 30000
                    powerup = None
                    snake.pop()
                else:
                    snake.pop()

    if screen_state == "menu":
        draw_menu()
    elif screen_state == "game":
        draw_game()
    elif screen_state == "gameover":
        draw_gameover()
    elif screen_state == "leaderboard":
        draw_leaderboard()
    elif screen_state == "settings":
        draw_settings()

    pygame.display.flip()

pygame.quit()
