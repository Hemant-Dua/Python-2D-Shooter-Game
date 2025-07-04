import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Set up the display with a border
border_width = 20  # Adjust border width as needed
width, height = 800, 600
screen_width = width + 2 * border_width
screen_height = height + 2 * border_width
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python 2D Shooter")

# Load images
player_image = pygame.image.load("Assets/sprites/player.webp")
player_image = pygame.transform.scale(player_image, (70, 70))
spider_image = pygame.image.load("Assets/sprites/spider.png")
spider_image = pygame.transform.scale(spider_image, (50, 50))

#Sounds
shoot_sound = pygame.mixer.Sound("Assets/sound/laser.mp3")
pipe = pygame.mixer.Sound("Assets/sound/metal_pipe_meme.mp3")
fart = pygame.mixer.Sound("Assets/sound/fart_meme.mp3")
game_end = pygame.mixer.Sound("Assets/sound/GameEnd.mp3")
damage = pygame.mixer.Sound("Assets/sound/damage.mp3")
background_music = pygame.mixer.Sound("Assets/sound/bgScore.mp3")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (204, 204, 204)
BG = (170, 128, 255)

# Fonts
font = pygame.font.Font(None, 36)
title = pygame.font.Font(None, 72)

# Start Screen
def start_screen():
  start_screen_active = True
  while start_screen_active:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          start_screen_active = False

    screen.fill(BG)
    title_text = title.render("Python 2D Shooter", True, WHITE)
    title_rect = title_text.get_rect()
    title_rect.center = (width // 2, height // 2 - 70)
    screen.blit(title_text, title_rect)


    # Add instructions below the start text
    instructions_text = font.render(" **INSTRUCTIONS: Use Arrow keys to move and Space to shoot** ", True, (242, 242, 242))
    instructions_rect = instructions_text.get_rect()
    instructions_rect.center = (width // 2, height // 2)
    screen.blit(instructions_text, instructions_rect)

    start_text = font.render("Press SPACE to Start", True, GRAY)
    text_rect = start_text.get_rect()
    text_rect.center = (width // 2, height // 2 + 150)
    screen.blit(start_text, text_rect)
    
    pygame.display.update()

# Game Loop
def game_loop():
    global player_x, player_y, player_health, enemy_x, enemy_y, enemy_health, bullets, score

    player_x, player_y = width // 2, height // 2
    player_health = 100
    bullet_speed = 10
    enemy_x, enemy_y = random.randint(border_width, screen_width - border_width - spider_image.get_width()), random.randint(border_width, screen_height - border_width - spider_image.get_height())
    enemy_health = 50
    bullets = []
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dx = enemy_x - player_x
                    dy = enemy_y - player_y
                    angle = math.atan2(dy, dx)
                    bullet_x = player_x + 25 + math.cos(angle) * 25
                    bullet_y = player_y + 25 + math.sin(angle) * 25
                    bullets.append([bullet_x, bullet_y, angle])
                    shoot_sound.play()

        # Player movement (consider border collisions)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > border_width:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_image.get_width() - border_width:
            player_x += 5
        if keys[pygame.K_UP] and player_y > border_width:
            player_y -= 5
        if keys[pygame.K_DOWN] and player_y < screen_height - player_image.get_height() - border_width:
            player_y += 5

        # Enemy movement (simple AI)
        if enemy_x < player_x:
            enemy_x += 2
        elif enemy_x > player_x:
            enemy_x -= 2
        if enemy_y < player_y:
            enemy_y += 2
        elif enemy_y > player_y:
            enemy_y -= 2

        # Bullet movement
        for bullet in bullets:
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])
            if not 0 <= bullet[0] <= width or not 0 <= bullet[1] <= height:
                bullets.remove(bullet)

        # Bullet-enemy collision
        for bullet in bullets:
            if (
                bullet[0] > enemy_x
                and bullet[0] < enemy_x + 50
                and bullet[1] > enemy_y
                and bullet[1] < enemy_y + 50
            ):
                enemy_health -= 10
                bullets.remove(bullet)

        # Check for enemy death
        if enemy_health <= 0:
            score += 10
            enemy_x, enemy_y = random.randint(border_width, screen_width - border_width - spider_image.get_width()), random.randint(border_width, screen_height - border_width - spider_image.get_height())
            enemy_health = 50

        # Collision detection (simplified)
        if (
            player_x < enemy_x + 50
            and player_x + 50 > enemy_x
            and player_y < enemy_y + 50
            and player_y + 50 > enemy_y
        ):
            player_health -= 10
            damage.play()
            enemy_health -= 20

        # Check for game over
        if player_health <= 0:
            running = False

        # Clear the screen
        screen.fill(BG)

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Draw enemy
        screen.blit(spider_image, (enemy_x, enemy_y))

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 3)

        # Draw health bars with borders
        # Player health bar
        player_health_bar_width = 200  # Define a fixed width for the player's health bar
        pygame.draw.rect(screen, WHITE, (border_width + 18, border_width + 18, player_health_bar_width + 4, 24), 2)  # Border
        pygame.draw.rect(screen, GREEN, (border_width + 20, border_width + 20, player_health * (player_health_bar_width / 100), 20)) 

        # Enemy health bar
        enemy_health_bar_width = 100  # Define a fixed width for the enemy's health bar (half of player's)
        pygame.draw.rect(screen, WHITE, (screen_width - border_width - 20 - enemy_health_bar_width - 4, border_width + 18, enemy_health_bar_width + 4, 24), 2)  # Border
        pygame.draw.rect(screen, RED, (screen_width - border_width - 20 - enemy_health_bar_width, border_width + 20, enemy_health * (enemy_health_bar_width / 100), 20))
        
        # Draw score
        score_text = font.render("Score: " + str(score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.centerx = screen_width // 2
        screen.blit(score_text, score_rect)

        # Update the display
        pygame.display.update()

        # Control game speed
        time.sleep(0.01)

    return score

# End Screen
def end_screen(score):
    end_screen_active = True
    pipe.play()
    while end_screen_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(BLACK)
        game_over_text = title.render("Game Over!", True, RED)
        score_text = font.render("Your Score: " + str(score), True, WHITE)
        game_over_rect = game_over_text.get_rect()
        score_rect = score_text.get_rect()
        game_over_rect.center = (width // 2, height // 2 - 30)
        score_rect.center = (width // 2, height // 2 + 30)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        pygame.display.update()
        

# Main Game
if __name__ == "__main__":
    background_music.play(loops=-1)
    start_screen()
    final_score = game_loop()
    background_music.stop()
    end_screen(final_score)

# Quit Pygame
pygame.quit()