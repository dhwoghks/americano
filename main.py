import pygame
import random
import math

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivors Lite")

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 플레이어 설정
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# 적 설정
enemy_size = 30
enemy_list = []
enemy_speed = 3

# 게임 변수
clock = pygame.time.Clock()
FPS = 60
score = 0

# 충돌 판정 함수
def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos
    distance = math.sqrt((p_x - e_x) ** 2 + (p_y - e_y) ** 2)
    return distance < (player_size / 2 + enemy_size / 2)

# 적 생성 함수
def spawn_enemy():
    x_pos = random.randint(-enemy_size, WIDTH)  # 화면 바깥쪽 좌우에서 적의 x 위치 생성
    y_pos = random.choice([-enemy_size, HEIGHT])  # 화면 바깥쪽 상단 또는 하단에서 적의 y 위치 생성
    enemy_list.append([x_pos, y_pos])

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # 적 생성 및 이동
    if random.random() < 0.02:  # 적이 나타날 확률
        spawn_enemy()

    for enemy in enemy_list:
        # 적이 플레이어를 향해 이동
        direction = [player_pos[0] - enemy[0], player_pos[1] - enemy[1]]
        distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        direction = [direction[0] / distance, direction[1] / distance]
        enemy[0] += direction[0] * enemy_speed
        enemy[1] += direction[1] * enemy_speed

        # 충돌 판정
        if detect_collision(player_pos, enemy):
            running = False  # 게임 종료

    # 화면 그리기
    screen.fill(WHITE)
    pygame.draw.circle(screen, GREEN, (player_pos[0], player_pos[1]), player_size // 2)
    for enemy in enemy_list:
        pygame.draw.circle(screen, RED, (int(enemy[0]), int(enemy[1])), enemy_size // 2)

    # 점수 표시
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 속도 조절
    clock.tick(FPS)

    # 점수 증가
    score += 1

# 게임 종료
pygame.quit()
