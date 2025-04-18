from db import get_or_create_user, save_score

user_id = get_or_create_user()  # Ойын басталғанда сұрайды
import pygame
import random
import sys
import time

pygame.init()
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FPS = 120

FOOD_COLORS = {
    1: (255, 0, 0),
    2: (255, 165, 0),
    3: (255, 255, 0)
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont("Times New Roman", 20, True, True) # --> SysFont, системные шрифты    Жирный, Курсив
clock = pygame.time.Clock()

snake = [(300, 300), (280, 300), (260, 300)]
snake_direction = (20, 0)

food_pos = None
food_weight = 1
food_spawn_time = 0

score = 0
level = 1
speed = 10

def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if(x, y) not in snake:
            return (x, y), random.choice([1, 2, 3])
        
food_pos, food_weight = generate_food()
food_spawn_time = time.time()

while True:

    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_direction != (0, 20):
        snake_direction = (0, -20)
    if keys[pygame.K_DOWN] and snake_direction != (0, -20):
        snake_direction = (0, 20)
    if keys[pygame.K_LEFT] and snake_direction != (20, 0):
        snake_direction = (-20, 0)
    if keys[pygame.K_RIGHT] and snake_direction != (-20, 0):
        snake_direction = (20, 0)
    
    new_head = (
        snake[0][0] + snake_direction[0],  # X
        snake[0][1] + snake_direction[1]   # Y
    )
    
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake
    ):
        break

    snake.insert(0, new_head)

    if new_head == food_pos:
        score += food_weight
        food_pos, food_weight = generate_food()
        food_spawn_time = time.time()
        if score // 4 + 1 > level:
            level += 1
            speed += 2
    else:
        snake.pop()
    
    if time.time() - food_spawn_time >= 5:
        food_pos, food_weight = generate_food()
        food_spawn_time = time.time()
    
    
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    food_color = FOOD_COLORS[food_weight]
    pygame.draw.rect(screen, food_color, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    score_text = font.render(f"Счет: {score}", True, BLACK)
    level_text = font.render(f"Уровень: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(speed)


save_score(user_id, level, score)