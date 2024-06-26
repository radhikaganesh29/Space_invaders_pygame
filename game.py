import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BULLET_SIZE = 10
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 7

# File to store high score
HIGH_SCORE_FILE = 'high_score.txt'

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
player_img = pygame.image.load('assets/images/player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))
enemy_img = pygame.image.load('assets/images/enemy.png').convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))

# Load sounds
shoot_sound = pygame.mixer.Sound('assets/sounds/shoot.wav')
explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')

# Clock for controlling the game's frame rate
clock = pygame.time.Clock()

# Game variables
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT - 2 * PLAYER_SIZE
player_speed_x = 0
enemies = []
bullets = []
score = 0
game_over = False
paused = False

# Function to draw the player on the screen
def draw_player(x, y):
    screen.blit(player_img, (x, y))

# Function to draw an enemy on the screen
def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Function to handle shooting
def shoot_bullet(x, y):
    bullets.append({'x': x + PLAYER_SIZE // 2 - BULLET_SIZE // 2, 'y': y - BULLET_SIZE})

# Function to check collisions between two rectangles
def is_collision(obj1_x, obj1_y, obj1_size, obj2_x, obj2_y, obj2_size):
    if obj1_x < obj2_x + obj2_size and obj1_x + obj1_size > obj2_x and obj1_y < obj2_y + obj2_size and obj1_y + obj1_size > obj2_y:
        return True
    return False

# Function to display text on screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Function to load high score from file
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

# Function to save high score to file
def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))

# Load initial high score
high_score = load_high_score()

# Game loop
while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Player movement controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed_x = -PLAYER_SPEED
            elif event.key == pygame.K_RIGHT:
                player_speed_x = PLAYER_SPEED
            elif event.key == pygame.K_SPACE:
                if len(bullets) < 5 and not paused:  # Limit bullets on screen and prevent shooting when paused
                    shoot_sound.play()
                    shoot_bullet(player_x, player_y)
            elif event.key == pygame.K_p:  # Pause game when 'P' key is pressed
                paused = not paused
                pygame.mixer.pause()  # Pause all sounds

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_speed_x = 0

    # Pause screen
    if paused:
        screen.fill(BLACK)
        draw_text("PAUSED", pygame.font.Font(None, 72), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        continue  # Skip the rest of the game loop if paused

    # Update player position
    player_x += player_speed_x

    # Ensure player stays within screen bounds
    if player_x < 0:
        player_x = 0
    elif player_x > SCREEN_WIDTH - PLAYER_SIZE:
        player_x = SCREEN_WIDTH - PLAYER_SIZE

    # Generate enemies
    if len(enemies) < 10:  # Limit number of enemies on screen
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemy_y = random.randint(50, 200)
        enemies.append({'x': enemy_x, 'y': enemy_y})

    # Update enemies position and check collisions with player
    for enemy in enemies[:]:
        enemy['y'] += ENEMY_SPEED

        # Check collision with player
        if is_collision(player_x, player_y, PLAYER_SIZE, enemy['x'], enemy['y'], ENEMY_SIZE):
            explosion_sound.play()
            game_over = True
            break

        # Remove enemies that have moved off screen
        if enemy['y'] > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # Update bullets position and check collisions with enemies
    for bullet in bullets[:]:
        bullet['y'] -= BULLET_SPEED

        # Check collision with enemies
        for enemy in enemies[:]:
            if is_collision(bullet['x'], bullet['y'], BULLET_SIZE, enemy['x'], enemy['y'], ENEMY_SIZE):
                explosion_sound.play()
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 20  # Increase score for each enemy destroyed

        # Remove bullets that have moved off screen
        if bullet['y'] < 0:
            bullets.remove(bullet)

    # Update high score if current score is higher
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Clear screen
    screen.fill(BLACK)

    # Draw player and enemies
    draw_player(player_x, player_y)
    for enemy in enemies:
        draw_enemy(enemy['x'], enemy['y'])

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet['x'], bullet['y'], BULLET_SIZE, BULLET_SIZE))

    # Display score and high score
    draw_text(f"Score: {score}", pygame.font.Font(None, 36), WHITE, 70, 10)
    draw_text(f"High Score: {high_score}", pygame.font.Font(None, 36), WHITE, SCREEN_WIDTH - 150, 10)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
draw_text("GAME OVER", pygame.font.Font(None, 72), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Quit Pygame
pygame.quit()
