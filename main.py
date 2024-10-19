import pygame
import random
import math

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivors Lite")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 플레이어 설정
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_health = 5
player_speed = 5

# 적 설정
enemy_size = 30
enemy_list = []  # 각 적의 체력을 포함한 리스트
enemy_speed = 1.5

# 총알 설정
bullet_size = 5
bullet_speed = 10
bullets = []
bullet_cooldown = 100  # 총알 발사 쿨타임 (밀리초)
last_bullet_time = 0

# 게임 변수
clock = pygame.time.Clock()
FPS = 60
score = 0
enemy_spawn_time = 1000  # 적 생성 간격 (밀리초)
last_enemy_spawn_time = pygame.time.get_ticks()

# 충돌 판정 함수
def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos
    distance = math.sqrt((p_x - e_x) ** 2 + (p_y - e_y) ** 2)
    return distance < (player_size / 2 + enemy_size / 2)

# 하트 그리기 함수
def draw_heart(surface, position):
    heart_points = [
        (position[0] + 10, position[1] + 20),
        (position[0], position[1] + 10),
        (position[0] + 5, position[1]),
        (position[0] + 10, position[1] + 5),
        (position[0] + 15, position[1]),
        (position[0] + 20, position[1] + 10),
        (position[0] + 10, position[1] + 20)
    ]
    pygame.draw.polygon(surface, RED, heart_points)

# 적 생성 함수
def spawn_enemy():
    direction = random.choice(['left', 'right', 'top', 'bottom'])
    enemy_health = 3  # 각 적의 체력 설정

    if direction == 'left':
        x_pos = random.randint(-enemy_size, 0)
        y_pos = random.randint(0, HEIGHT)
    elif direction == 'right':
        x_pos = random.randint(WIDTH, WIDTH + enemy_size)
        y_pos = random.randint(0, HEIGHT)
    elif direction == 'top':
        x_pos = random.randint(0, WIDTH)
        y_pos = random.randint(-enemy_size, 0)
    else:  # direction == 'bottom'
        x_pos = random.randint(0, WIDTH)
        y_pos = random.randint(HEIGHT, HEIGHT + enemy_size)

    enemy_list.append({'pos': [x_pos, y_pos], 'health': enemy_health})  # 적의 위치와 체력을 딕셔너리로 저장

# 총알 생성 함수
def spawn_bullet(player_pos, direction):
    bullet_pos = [player_pos[0], player_pos[1]]
    bullets.append((bullet_pos, direction))

#아이템 설정
item_size = 20
item_list = []
item_spawn_time = 5000  # 아이템 생성 간격 (밀리초)
last_item_spawn_time = pygame.time.get_ticks()  # 마지막 아이템 생성 시간

#아이템 생성 함수
def spawn_item():
    x_pos = random.randint(0, WIDTH)
    y_pos = random.randint(0, HEIGHT)
    item_list.append([x_pos, y_pos])  # 아이템의 위치 추가
# 게임 루프
running = True
game_over = False
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if not game_over:
        # 플레이어 이동
        if keys[pygame.K_w] and player_pos[1] > player_size // 2:
            player_pos[1] -= player_speed
        if keys[pygame.K_s] and player_pos[1] < HEIGHT - player_size // 2:
            player_pos[1] += player_speed
        if keys[pygame.K_a] and player_pos[0] > player_size // 2:
            player_pos[0] -= player_speed
        if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size // 2:
            player_pos[0] += player_speed
        
        # 총알 발사
        direction = None
        if keys[pygame.K_UP]:
            direction = [0, -1]
        elif keys[pygame.K_DOWN]:
            direction = [0, 1]
        elif keys[pygame.K_LEFT]:
            direction = [-1, 0]
        elif keys[pygame.K_RIGHT]:
            direction = [1, 0]

        current_time = pygame.time.get_ticks()  # 현재 시간 가져오기
        if direction and (current_time - last_bullet_time > bullet_cooldown):
            spawn_bullet(player_pos, direction)
            last_bullet_time = current_time

        # 총알 이동 및 충돌 처리
        for bullet in bullets[:]:
            bullet_pos, bullet_direction = bullet
            bullet_pos[0] += bullet_direction[0] * bullet_speed
            bullet_pos[1] += bullet_direction[1] * bullet_speed
            if bullet_pos[1] < 0 or bullet_pos[1] > HEIGHT or bullet_pos[0] < 0 or bullet_pos[0] > WIDTH:
                bullets.remove(bullet)
                continue

            for enemy in enemy_list[:]:
                if detect_collision(bullet_pos, enemy['pos']):  # 적의 위치에 접근
                    enemy['health'] -= 1  # 적의 체력 감소
                    bullets.remove(bullet)
                    if enemy['health'] <= 0:
                        enemy_list.remove(enemy)
                    break

        # 적 생성 및 이동
        if current_time - last_enemy_spawn_time > enemy_spawn_time:
            spawn_enemy()
            last_enemy_spawn_time = current_time

        for enemy in enemy_list:
            direction = [player_pos[0] - enemy['pos'][0], player_pos[1] - enemy['pos'][1]]
            distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            direction = [direction[0] / distance, direction[1] / distance]
            enemy['pos'][0] += direction[0] * enemy_speed
            enemy['pos'][1] += direction[1] * enemy_speed

            if detect_collision(player_pos, enemy['pos']):
                player_health -= 1
                enemy_list.remove(enemy)
                if player_health <= 0:
                    game_over = True
                break

    if current_time - last_item_spawn_time > item_spawn_time:
        spawn_item()
        last_item_spawn_time = current_time  # 마지막 아이템 생성 시간 업데이트

    # 아이템 그리기
    for item in item_list:
        pygame.draw.rect(screen, (0, 255, 255), (item[0], item[1], item_size, item_size))  # 아이템 표시

    # 플레이어와 아이템 충돌 체크
    for item in item_list[:]:
        if detect_collision(player_pos, item):  # 플레이어와 아이템 충돌 체크
            player_health += 1  # 체력 회복
            item_list.remove(item)  # 아이템 제거
            break
    # 화면 그리기
    screen.fill(WHITE)
    if game_over:
        # 게임 오버 화면
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
        
        # 재시작 및 종료 안내 문구
        restart_text = pygame.font.Font(None, 36).render("Press R to Restart or Q to Quit", True, (0, 0, 0))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
        
        # r 또는 q 버튼 입력 처리
        if keys[pygame.K_r]:
            player_pos = [WIDTH // 2, HEIGHT // 2]
            enemy_list.clear()
            score = 0
            player_health = 5
            game_over = False
        elif keys[pygame.K_q]:
            running = False
    else:
        # 플레이어와 적, 총알 그리기
        for i in range(player_health):
            draw_heart(screen, (10 + i * 30, 50))
        pygame.draw.circle(screen, GREEN, (player_pos[0], player_pos[1]), player_size // 2)
        for enemy in enemy_list:
            pygame.draw.circle(screen, RED, (int(enemy['pos'][0]), int(enemy['pos'][1])), enemy_size // 2)
        
        # 총알 그리기
        for bullet in bullets:
            pygame.draw.circle(screen, (0, 0, 255), (int(bullet[0][0]), int(bullet[0][1])), bullet_size)

        # 점수 표시
        score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
    
    
    # 화면 업데이트
    pygame.display.flip()
    clock.tick(FPS)

    # 점수 증가
    if not game_over:
        score += 1

# 게임 종료
pygame.quit()
