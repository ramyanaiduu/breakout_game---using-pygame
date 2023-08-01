import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
BRICK_WIDTH = 80
BRICK_HEIGHT = 20
BRICK_GAP = 4
NUM_BRICKS_ROW = 10
NUM_BRICKS_COL = 6
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def draw_paddle(paddle_x):
    pygame.draw.rect(screen, BLUE, (paddle_x, SCREEN_HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

def draw_brick(brick_x, brick_y):
    pygame.draw.rect(screen, GREEN, (brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

def create_bricks():
    bricks = []
    for row in range(NUM_BRICKS_COL):
        for col in range(NUM_BRICKS_ROW):
            brick_x = col * (BRICK_WIDTH + BRICK_GAP)
            brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + 50
            bricks.append((brick_x, brick_y))
    return bricks

def handle_collision(ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x, paddle_y, bricks):
    # Check for collision with paddle
    if ball_y + BALL_RADIUS >= SCREEN_HEIGHT - PADDLE_HEIGHT and paddle_x - BALL_RADIUS <= ball_x <= paddle_x + PADDLE_WIDTH + BALL_RADIUS:
        ball_speed_y = -ball_speed_y

    # Check for collision with bricks
    for brick in bricks:
        brick_x, brick_y = brick
        if brick_x - BALL_RADIUS <= ball_x <= brick_x + BRICK_WIDTH + BALL_RADIUS and brick_y - BALL_RADIUS <= ball_y <= brick_y + BRICK_HEIGHT + BALL_RADIUS:
            ball_speed_y = -ball_speed_y
            bricks.remove(brick)
            break

    # Check for collision with walls
    if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
        ball_speed_x = -ball_speed_x
    if ball_y <= BALL_RADIUS:
        ball_speed_y = -ball_speed_y

    return ball_speed_x, ball_speed_y, bricks

def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 40))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

def game_loop():
    paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT

    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_speed_x = random.choice([-4, -3, 3, 4])
    ball_speed_y = -4

    bricks = create_bricks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 5
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            paddle_x += 5

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        ball_speed_x, ball_speed_y, bricks = handle_collision(ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x, paddle_y, bricks)

        screen.fill(BLACK)
        draw_paddle(paddle_x)
        draw_ball(ball_x, ball_y)

        for brick in bricks:
            draw_brick(brick[0], brick[1])

        if ball_y >= SCREEN_HEIGHT:
            game_over()

        if not bricks:
            font = pygame.font.Font(None, 74)
            text = font.render("You Win!", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40))
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()
