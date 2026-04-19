import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 100, 200)

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

MUSIC_FOLDER = "/Users/zere/Desktop/labs/practice9/music_player/music"
tracks = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
tracks.sort()

current = 0
playing = False

def load_track(index):
    path = os.path.join(MUSIC_FOLDER, tracks[index])
    pygame.mixer.music.load(path)

def draw():
    screen.fill(WHITE)

    title = font.render("Music Player", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    track_name = tracks[current] if tracks else "Нет треков"
    name = small_font.render(track_name, True, BLACK)
    screen.blit(name, (WIDTH // 2 - name.get_width() // 2, 100))

    status = "Playing" if playing else "Stopped"
    status_text = font.render(status, True, BLACK)
    screen.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 150))

    controls = small_font.render("P=Play  S=Stop  N=Next  B=Previous  Q=Quit", True, GRAY)
    screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, 350))

    pygame.display.flip()

load_track(current)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.mixer.music.play()
                playing = True

            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                playing = False

            elif event.key == pygame.K_n:
                current = (current + 1) % len(tracks)
                load_track(current)
                if playing:
                    pygame.mixer.music.play()

            elif event.key == pygame.K_b:
                current = (current - 1) % len(tracks)
                load_track(current)
                if playing:
                    pygame.mixer.music.play()

            elif event.key == pygame.K_q:
                running = False

    draw()
    clock.tick(60)

pygame.quit()