def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# main.py
import pygame
import sys
import os
from settings import *
from utils import play_music, load_sfx, load_json
from player import Player
from level import Level
from ui import draw_text
from obstacles import ObstacleManager


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Geometry Dash - Clone ')

# load assets
ASSETS = os.path.join(os.path.dirname(__file__), '..', 'assets')
LEVELS = os.path.join(os.path.dirname(__file__), '..', 'levels')

score_sfx = load_sfx(os.path.join(ASSETS, 'score.wav'))
background_img_path = os.path.join(ASSETS, 'background.png')
background_img = None
if os.path.exists(background_img_path):
    background_img = pygame.image.load(background_img_path).convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bg_music = os.path.join(ASSETS, 'bg_music.mp3')
jump_sfx = load_sfx(os.path.join(ASSETS, 'jump.wav'))
hit_sfx = load_sfx(os.path.join(ASSETS, 'hit.wav'))
player_img_path = os.path.join(ASSETS, 'player.png')
player_sprite = None
if os.path.exists(player_img_path):
    player_sprite = pygame.image.load(player_img_path).convert_alpha()
    player_sprite = pygame.transform.scale(player_sprite, (PLAYER_SIZE, PLAYER_SIZE))

# load levels
level_files = [os.path.join(LEVELS, f) for f in os.listdir(LEVELS) if f.endswith('.json')]
levels = [Level(f) for f in level_files]

# play background music for menu
try:
    play_music(bg_music)
except Exception:
    pass

# game state
state = 'menu'  # menu, running, paused, gameover, level_select
current_level_idx = 0
player = Player(sprite=player_sprite)
ob_manager = ObstacleManager()

speed = SPEED_START
distance = 0
score = 0
highscore = 0
score_100_played = False
highscore = load_highscore()

# menu helpers
selected_level = 0

# prepare first level
if levels:
    levels[0].prepare(start_x=WIDTH+200)

# transitions
fade_alpha = 0
fading = False

next_score_sound = 100
last_score_sound = 0  # Add this before the main loop

# main loop
# ...existing code...

bg_scroll = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == 'running':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.on_ground:
                    player.jump()
                    if jump_sfx:
                        jump_sfx.play()
        elif state == 'menu':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and levels:
                    state = 'running'
                    player = Player(sprite=player_sprite)
                    levels[current_level_idx].prepare(start_x=WIDTH+200)
                    score = 0
                    distance = 0
                    next_score_sound = 100
                    last_score_sound = 0
    # Move background (parallax effect)
    if state == 'running':
        bg_scroll -= SPEED_START // 4  # Move slower than obstacles for parallax
        if abs(bg_scroll) >= WIDTH:
            bg_scroll = 0

    # Draw background
    if background_img:
        screen.blit(background_img, (bg_scroll, 0))
        screen.blit(background_img, (bg_scroll + WIDTH, 0))
    else:
        screen.fill((30, 30, 35))

    # Draw ground/path (always draw, not just in else)
    ground_height = 40  # Thickness of the ground
    pygame.draw.rect(screen, (60, 60, 60), (0, GROUND_Y, WIDTH, ground_height))

    if state == 'menu':
        draw_text(screen, "GEOMETRY DASH", WIDTH//2, HEIGHT//2-60, size=48, center=True)
        draw_text(screen, "Press ENTER to Start", WIDTH//2, HEIGHT//2, size=28, center=True)
    elif state == 'running':
        # Update
        player.update()
        levels[current_level_idx].update(SPEED_START)
        distance += SPEED_START
        score = distance // 30  # Increases 3x slower
        if score % 100 == 0 and score != 0 and score != last_score_sound:
           if score_sfx:
             score_sfx.play()
           last_score_sound = score
        # Collision detection
        for ob in levels[current_level_idx].ob_manager.items:
            if player.rect.colliderect(ob.rect):
                if hit_sfx:
                    hit_sfx.play()
                state = 'gameover'
        # Draw
        levels[current_level_idx].draw(screen)
        player.draw(screen)
        draw_text(screen, f"Score: {score}", 20, 20, size=24)
        draw_text(screen, f"High Score: {highscore}", 20, 50, size=24)
    elif state == 'gameover':
        draw_text(screen, "GAME OVER", WIDTH//2, HEIGHT//2-40, size=48, center=True)
        draw_text(screen, "Press ENTER for Menu", WIDTH//2, HEIGHT//2, size=28, center=True)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            state = 'menu'
        if score > highscore:
            highscore = score
            save_highscore(highscore)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()