import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 游戏窗口大小
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


# 设置窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('贪食蛇')
clock = pygame.time.Clock()

# 地图障碍物（仅中间横线障碍）
OBSTACLE_COLOR = (120, 120, 120)
obstacles = []
# 只保留中间一条横线障碍
for i in range(5 * CELL_SIZE, WIDTH - 5 * CELL_SIZE, CELL_SIZE):
    obstacles.append((i, HEIGHT // 2))

# 蛇的初始状态
snake = [(100, 100), (80, 100), (60, 100)]
direction = 'RIGHT'
change_to = direction

# 食物
food_pos = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
food_spawn = True

score = 0

def show_score():
    font = pygame.font.SysFont('Arial', 24)
    score_surface = font.render(f'Scores: {score}', True, BLACK)
    screen.blit(score_surface, (10, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to
    x, y = snake[0]

    if direction == 'UP':
        y -= CELL_SIZE
    elif direction == 'DOWN':
        y += CELL_SIZE
    elif direction == 'LEFT':
        x -= CELL_SIZE
    elif direction == 'RIGHT':
        x += CELL_SIZE

    # 穿墙处理
    x = x % WIDTH
    y = y % HEIGHT
    new_head = (x, y)


    # 判断是否撞到自己或障碍物
    if new_head in snake or new_head in obstacles:
        break

    snake.insert(0, new_head)

    # 吃到食物
    if new_head == food_pos:
        score += 1
        food_spawn = False
    else:
        snake.pop()

    if not food_spawn:
        food_pos = (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)
        food_spawn = True


    screen.fill(WHITE)
    # 绘制背景网格
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

    # 绘制障碍物
    for obs in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, pygame.Rect(obs[0], obs[1], CELL_SIZE, CELL_SIZE))

    # 绘制蛇：蛇头有眼睛，蛇身渐变色，带边框
    if snake:
        # 颜色渐变（从深到浅）
        body_colors = [(60, 180, 60), (100, 220, 100), (150, 255, 150)]
        # 蛇头
        head = snake[0]
        pygame.draw.ellipse(screen, (0, 120, 0), pygame.Rect(head[0], head[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.ellipse(screen, (30, 80, 30), pygame.Rect(head[0], head[1], CELL_SIZE, CELL_SIZE), 2)  # 头部边框
        # 眼睛
        eye_radius = 3
        offset = 5
        if len(snake) > 1:
            hx, hy = head
            nx, ny = snake[1]
            dx, dy = hx - nx, hy - ny
            if dx > 0:  # 向右
                eye1 = (hx + CELL_SIZE - offset, hy + offset)
                eye2 = (hx + CELL_SIZE - offset, hy + CELL_SIZE - offset)
            elif dx < 0:  # 向左
                eye1 = (hx + offset, hy + offset)
                eye2 = (hx + offset, hy + CELL_SIZE - offset)
            elif dy > 0:  # 向下
                eye1 = (hx + offset, hy + CELL_SIZE - offset)
                eye2 = (hx + CELL_SIZE - offset, hy + CELL_SIZE - offset)
            else:  # 向上
                eye1 = (hx + offset, hy + offset)
                eye2 = (hx + CELL_SIZE - offset, hy + offset)
        else:
            eye1 = (head[0] + offset, head[1] + offset)
            eye2 = (head[0] + CELL_SIZE - offset, head[1] + offset)
        pygame.draw.circle(screen, (255, 255, 255), eye1, eye_radius)
        pygame.draw.circle(screen, (0, 0, 0), eye1, 1)
        pygame.draw.circle(screen, (255, 255, 255), eye2, eye_radius)
        pygame.draw.circle(screen, (0, 0, 0), eye2, 1)
        # 蛇身
        for idx, pos in enumerate(snake[1:]):
            color = body_colors[min(idx, len(body_colors)-1)]
            pygame.draw.ellipse(screen, color, pygame.Rect(pos[0]+2, pos[1]+4, CELL_SIZE-4, CELL_SIZE-8))
            pygame.draw.ellipse(screen, (60, 120, 60), pygame.Rect(pos[0]+2, pos[1]+4, CELL_SIZE-4, CELL_SIZE-8), 1)
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
    show_score()
    pygame.display.flip()
    clock.tick(10)

# 游戏结束
font = pygame.font.SysFont('Arial', 48)
game_over_surface = font.render('Game Over!', True, RED)
game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(game_over_surface, game_over_rect)
show_score()
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()
