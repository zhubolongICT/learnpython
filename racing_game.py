import pygame
import sys
import random

# 初始化
pygame.init()
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD_COLOR = (50, 50, 50)
CAR_COLOR = (0, 180, 255)
ENEMY_COLOR = (255, 80, 80)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simple Racing Game')
clock = pygame.time.Clock()

# 玩家车辆
car_width, car_height = 50, 90
player = pygame.Rect(WIDTH//2 - car_width//2, HEIGHT - car_height - 20, car_width, car_height)
player_speed = 7

# 敌方车辆
enemy_width, enemy_height = 50, 90
enemies = []
enemy_speed = 6
enemy_spawn_delay = 40
spawn_counter = 0

score = 0
font = pygame.font.SysFont('Arial', 24)

# 赛道线
lane_width = 80
lane_x = [WIDTH//2 - lane_width, WIDTH//2, WIDTH//2 + lane_width]

def draw():
    screen.fill(WHITE)
    # 画赛道
    pygame.draw.rect(screen, ROAD_COLOR, (WIDTH//2 - 120, 0, 240, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 2, y, 4, 20))
    # 画玩家车
    pygame.draw.rect(screen, CAR_COLOR, player, border_radius=10)
    # 画敌人车
    for e in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, e, border_radius=10)
    # 分数
    score_surf = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_surf, (10, 10))
    pygame.display.flip()

def move_enemies():
    global enemies
    for e in enemies:
        e.move_ip(0, enemy_speed)
    enemies = [e for e in enemies if e.top < HEIGHT]

def check_collisions():
    global enemies, score
    for e in enemies[:]:
        if player.colliderect(e):
            return True
        if e.bottom >= HEIGHT:
            enemies.remove(e)
            score += 1
    return False

def main():
    global spawn_counter
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > WIDTH//2 - 120:
            player.move_ip(-player_speed, 0)
        if keys[pygame.K_RIGHT] and player.right < WIDTH//2 + 120:
            player.move_ip(player_speed, 0)
        move_enemies()
        spawn_counter += 1
        if spawn_counter >= enemy_spawn_delay:
            lane = random.choice(lane_x)
            enemies.append(pygame.Rect(lane + lane_width//2 - enemy_width//2, -enemy_height, enemy_width, enemy_height))
            spawn_counter = 0
        if check_collisions():
            running = False
        draw()
    # 游戏结束
    over_surf = font.render('Game Over', True, (200, 0, 0))
    screen.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
