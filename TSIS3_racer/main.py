import pygame
import random
import json
import datetime

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer TSIS3")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 220, 0)
GOLD = (255, 140, 0)
CYAN = (0, 255, 255)
GREEN = (50, 200, 50)
BLUE = (50, 100, 200)
ORANGE = (255, 165, 0)
PURPLE = (150, 0, 200)
BROWN = (139, 69, 19)
LIGHT_GRAY = (180, 180, 180)

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 30)
tiny_font = pygame.font.SysFont(None, 24)

ROAD_LEFT = 75
ROAD_RIGHT = WIDTH - 75
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT


def load_settings():
    with open("settings.json", "r") as f:
        return json.load(f)


def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f, indent=4)


def load_leaderboard():
    with open("leaderboard.json", "r") as f:
        return json.load(f)


def save_leaderboard(lb):
    lb.sort(key=lambda x: x["score"], reverse=True)
    with open("leaderboard.json", "w") as f:
        json.dump(lb[:10], f, indent=4)


settings = load_settings()

screen_state = "menu"
username_input = ""
username = ""
final_score = 0
final_coins = 0
final_distance = 0


def reset_game():
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 120, 50, 80)
    enemies = []
    coins = []
    powerups = []
    obstacles = []
    road_lines = [i * 100 for i in range(7)]
    score = 0
    coin_count = 0
    distance = 0
    speed = 4
    spawn_timer = 0
    coin_timer = 0
    obs_timer = 0
    powerup_timer = 0
    active_powerup = None
    powerup_end = 0
    shield = False
    nitro = False
    return (player, enemies, coins, powerups, obstacles, road_lines,
            score, coin_count, distance, speed, spawn_timer, coin_timer,
            obs_timer, powerup_timer, active_powerup, powerup_end, shield, nitro)


(player, enemies, coins, powerups, obstacles, road_lines,
 score, coin_count, distance, speed, spawn_timer, coin_timer,
 obs_timer, powerup_timer, active_powerup, powerup_end, shield, nitro) = reset_game()

game_over = False


def draw_button(text, x, y, w, h, color=GRAY, text_color=WHITE):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = small_font.render(text, True, text_color)
    screen.blit(label, (x + w // 2 - label.get_width() // 2,
                        y + h // 2 - label.get_height() // 2))
    return rect


def draw_menu():
    screen.fill(BLACK)
    title = font.render("RACER", True, RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    label = small_font.render("Введи имя:", True, WHITE)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 160))

    box = pygame.Rect(WIDTH // 2 - 90, 195, 180, 35)
    pygame.draw.rect(screen, WHITE, box, 2)
    name = small_font.render(username_input, True, WHITE)
    screen.blit(name, (box.x + 5, box.y + 7))

    play_btn = draw_button("Play", WIDTH // 2 - 70, 255, 140, 40, BLUE)
    lb_btn = draw_button("Leaderboard", WIDTH // 2 - 70, 310, 140, 40, DARK_GRAY)
    set_btn = draw_button("Settings", WIDTH // 2 - 70, 365, 140, 40, DARK_GRAY)
    quit_btn = draw_button("Quit", WIDTH // 2 - 70, 420, 140, 40, RED)
    return play_btn, lb_btn, set_btn, quit_btn


def draw_game():
    screen.fill(DARK_GRAY)
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    road_speed = speed + (2 if nitro else 0)
    for i in range(len(road_lines)):
        road_lines[i] += road_speed
        if road_lines[i] > HEIGHT:
            road_lines[i] = -100
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, road_lines[i], 10, 60))

    # Масляные пятна (препятствия)
    for obs in obstacles:
        pygame.draw.ellipse(screen, BROWN, obs)

    # Монеты
    for coin in coins:
        w = coin["weight"]
        color = YELLOW if w == 1 else (GOLD if w == 3 else CYAN)
        pygame.draw.ellipse(screen, color, coin["rect"])
        lbl = tiny_font.render(str(w), True, BLACK)
        screen.blit(lbl, (coin["rect"].x + 7, coin["rect"].y + 5))

    # Powerups
    for pu in powerups:
        color = ORANGE if pu["kind"] == "nitro" else (PURPLE if pu["kind"] == "shield" else GREEN)
        pygame.draw.rect(screen, color, pu["rect"], border_radius=5)
        lbl = tiny_font.render(pu["kind"][0].upper(), True, WHITE)
        screen.blit(lbl, (pu["rect"].x + 7, pu["rect"].y + 5))

    # Враги
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy, border_radius=6)

    # Игрок
    car_color = tuple(settings["car_color"])
    pygame.draw.rect(screen, car_color, player, border_radius=6)
    if shield:
        pygame.draw.rect(screen, PURPLE, player, 3)

    # HUD
    score_text = small_font.render(f"Score: {score}", True, WHITE)
    coin_text = small_font.render(f"Coins: {coin_count}", True, YELLOW)
    dist_text = tiny_font.render(f"Dist: {distance}m", True, WHITE)
    screen.blit(score_text, (5, 5))
    screen.blit(coin_text, (WIDTH - coin_text.get_width() - 5, 5))
    screen.blit(dist_text, (5, 30))

    if active_powerup:
        now = pygame.time.get_ticks()
        remaining = max(0, (powerup_end - now) // 1000)
        pu_text = tiny_font.render(f"{active_powerup}: {remaining}s", True, ORANGE)
        screen.blit(pu_text, (5, 50))

    if game_over:
        over = font.render("GAME OVER", True, RED)
        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 60))
        retry_btn = draw_button("Retry", WIDTH // 2 - 70, HEIGHT // 2, 140, 40, BLUE)
        menu_btn = draw_button("Menu", WIDTH // 2 - 70, HEIGHT // 2 + 55, 140, 40, DARK_GRAY)
        return retry_btn, menu_btn
    return None, None


def draw_gameover():
    screen.fill(BLACK)
    over = font.render("GAME OVER", True, RED)
    screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 80))

    s1 = small_font.render(f"Score: {final_score}", True, WHITE)
    s2 = small_font.render(f"Coins: {final_coins}", True, YELLOW)
    s3 = small_font.render(f"Distance: {final_distance}m", True, CYAN)
    screen.blit(s1, (WIDTH // 2 - s1.get_width() // 2, 180))
    screen.blit(s2, (WIDTH // 2 - s2.get_width() // 2, 220))
    screen.blit(s3, (WIDTH // 2 - s3.get_width() // 2, 260))

    retry_btn = draw_button("Retry", WIDTH // 2 - 70, 330, 140, 40, BLUE)
    menu_btn = draw_button("Main Menu", WIDTH // 2 - 70, 385, 140, 40, DARK_GRAY)
    return retry_btn, menu_btn


def draw_leaderboard():
    screen.fill(BLACK)
    title = font.render("TOP 10", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    lb = load_leaderboard()
    for i, entry in enumerate(lb):
        text = tiny_font.render(
            f"{i+1}. {entry['name']} — {entry['score']} ({entry['distance']}m)",
            True, WHITE
        )
        screen.blit(text, (15, 90 + i * 32))

    back_btn = draw_button("Back", WIDTH // 2 - 70, 530, 140, 40, DARK_GRAY)
    return back_btn


def draw_settings():
    screen.fill(BLACK)
    title = font.render("Settings", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    diff_color = BLUE
    diff_btn = draw_button(f"Diff: {settings['difficulty']}", WIDTH // 2 - 70, 140, 140, 40, diff_color)

    colors = {"Blue": [50, 150, 255], "Red": [220, 50, 50], "Green": [50, 200, 50]}
    color_btns = {}
    for i, (name, color) in enumerate(colors.items()):
        btn = draw_button(name, WIDTH // 2 - 70, 200 + i * 55, 140, 40, tuple(color))
        color_btns[name] = (btn, color)

    save_btn = draw_button("Save & Back", WIDTH // 2 - 70, 400, 140, 40, GREEN)
    return diff_btn, color_btns, save_btn


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

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
                    (player, enemies, coins, powerups, obstacles, road_lines,
                     score, coin_count, distance, speed, spawn_timer, coin_timer,
                     obs_timer, powerup_timer, active_powerup, powerup_end,
                     shield, nitro) = reset_game()
                    game_over = False
                    screen_state = "game"
                elif lb_btn.collidepoint(event.pos):
                    screen_state = "leaderboard"
                elif set_btn.collidepoint(event.pos):
                    screen_state = "settings"
                elif quit_btn.collidepoint(event.pos):
                    running = False

        elif screen_state == "gameover":
            if event.type == pygame.MOUSEBUTTONDOWN:
                retry_btn, menu_btn = draw_gameover()
                if retry_btn.collidepoint(event.pos):
                    (player, enemies, coins, powerups, obstacles, road_lines,
                     score, coin_count, distance, speed, spawn_timer, coin_timer,
                     obs_timer, powerup_timer, active_powerup, powerup_end,
                     shield, nitro) = reset_game()
                    game_over = False
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
                diff_btn, color_btns, save_btn = draw_settings()
                if diff_btn.collidepoint(event.pos):
                    options = ["easy", "normal", "hard"]
                    idx = options.index(settings["difficulty"])
                    settings["difficulty"] = options[(idx + 1) % len(options)]
                for name, (btn, color) in color_btns.items():
                    if btn.collidepoint(event.pos):
                        settings["car_color"] = color
                if save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    screen_state = "menu"

    # Игровая логика
    if screen_state == "game" and not game_over:
        diff_mult = {"easy": 0.7, "normal": 1.0, "hard": 1.4}[settings["difficulty"]]

        keys = pygame.key.get_pressed()
        player_speed = 5
        if keys[pygame.K_LEFT] and player.left > ROAD_LEFT:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < ROAD_RIGHT:
            player.x += player_speed

        distance += 1
        road_speed = int((4 + score // 5) * diff_mult) + (2 if nitro else 0)

        # Враги
        spawn_timer += 1
        spawn_interval = max(30, int(60 / diff_mult) - score // 3)
        if spawn_timer > spawn_interval:
            x = random.randint(ROAD_LEFT, ROAD_RIGHT - 50)
            enemies.append(pygame.Rect(x, -80, 50, 80))
            spawn_timer = 0

        for enemy in enemies[:]:
            enemy.y += road_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score += 1
            elif enemy.colliderect(player):
                if shield:
                    shield = False
                    active_powerup = None
                    enemies.remove(enemy)
                else:
                    final_score = score
                    final_coins = coin_count
                    final_distance = distance // 60
                    lb = load_leaderboard()
                    lb.append({
                        "name": username,
                        "score": score,
                        "coins": coin_count,
                        "distance": distance // 60,
                        "date": datetime.datetime.now().strftime("%Y-%m-%d")
                    })
                    save_leaderboard(lb)
                    screen_state = "gameover"

        # Монеты
        coin_timer += 1
        if coin_timer > 90:
            x = random.randint(ROAD_LEFT, ROAD_RIGHT - 25)
            w = random.choices([1, 3, 5], weights=[70, 20, 10])[0]
            coins.append({"rect": pygame.Rect(x, -30, 25, 25), "weight": w})
            coin_timer = 0

        for coin in coins[:]:
            coin["rect"].y += road_speed
            if coin["rect"].y > HEIGHT:
                coins.remove(coin)
            elif coin["rect"].colliderect(player):
                coins.remove(coin)
                coin_count += coin["weight"]
                score += coin["weight"]

        # Масляные пятна
        obs_timer += 1
        if obs_timer > 120:
            x = random.randint(ROAD_LEFT, ROAD_RIGHT - 40)
            obstacles.append(pygame.Rect(x, -20, 40, 20))
            obs_timer = 0

        for obs in obstacles[:]:
            obs.y += road_speed
            if obs.y > HEIGHT:
                obstacles.remove(obs)
            elif obs.colliderect(player):
                obstacles.remove(obs)
                speed = max(2, speed - 1)

        # Powerups
        powerup_timer += 1
        if powerup_timer > 200 and not powerups:
            x = random.randint(ROAD_LEFT, ROAD_RIGHT - 30)
            kind = random.choice(["nitro", "shield", "repair"])
            powerups.append({"rect": pygame.Rect(x, -30, 30, 30), "kind": kind})
            powerup_timer = 0

        now = pygame.time.get_ticks()
        for pu in powerups[:]:
            pu["rect"].y += road_speed
            if pu["rect"].y > HEIGHT:
                powerups.remove(pu)
            elif pu["rect"].colliderect(player):
                powerups.remove(pu)
                if pu["kind"] == "nitro":
                    nitro = True
                    active_powerup = "nitro"
                    powerup_end = now + 4000
                elif pu["kind"] == "shield":
                    shield = True
                    active_powerup = "shield"
                    powerup_end = now + 30000
                elif pu["kind"] == "repair":
                    speed = min(speed + 1, 10)
                    active_powerup = "repair"
                    powerup_end = now + 1000

        if active_powerup == "nitro" and now > powerup_end:
            nitro = False
            active_powerup = None

        speed = int((4 + score // 5) * diff_mult)

    # Отрисовка
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
