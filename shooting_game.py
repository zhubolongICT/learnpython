import pygame
import sys
import random

# 初始化
pygame.init()
WIDTH, HEIGHT = 480, 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 180, 255)
BULLET_COLOR = (255, 80, 80)
ENEMY_COLOR = (255, 180, 0)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simple Shooting Game')
clock = pygame.time.Clock()

# 玩家
player_size = (50, 30)
player = pygame.Rect(WIDTH//2 - player_size[0]//2, HEIGHT - 60, *player_size)
player_speed = 6

# 子弹
bullets = []
bullet_speed = -8

# 敌人
enemies = []
enemy_size = (40, 30)
enemy_speed = 3
enemy_spawn_delay = 40
spawn_counter = 0

score = 0
font = pygame.font.SysFont('Arial', 24)

def draw():
    screen.fill(WHITE)
    pygame.draw.rect(screen, PLAYER_COLOR, player)
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, b)
    for e in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, e)
    score_surf = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_surf, (10, 10))
    pygame.display.flip()

def move_bullets():
    global bullets
    for b in bullets:
        b.move_ip(0, bullet_speed)
    bullets = [b for b in bullets if b.bottom > 0]

def move_enemies():
    global enemies
    for e in enemies:
        e.move_ip(0, enemy_speed)
    enemies = [e for e in enemies if e.top < HEIGHT]

def check_collisions():
    global bullets, enemies, score
    for b in bullets[:]:
        for e in enemies[:]:
            if b.colliderect(e):
                bullets.remove(b)
                enemies.remove(e)
                score += 1
                break

def main():
    global spawn_counter
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.move_ip(-player_speed, 0)
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.move_ip(player_speed, 0)
        if keys[pygame.K_SPACE]:
            if not bullets or bullets[-1].top < player.top - 30:
                bullets.append(pygame.Rect(player.centerx - 3, player.top - 10, 6, 16))
        move_bullets()
        move_enemies()
        check_collisions()
        spawn_counter += 1
        if spawn_counter >= enemy_spawn_delay:
            x = random.randint(0, WIDTH - enemy_size[0])
            enemies.append(pygame.Rect(x, 0, *enemy_size))
            spawn_counter = 0
        # 检查敌人是否到达底部
        for e in enemies:
            if e.bottom >= HEIGHT:
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
