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
enemy_spawn_time = 1000  # 적 생성 간격 (밀리초)
last_enemy_spawn_time = pygame.time.get_ticks()  # 마지막 적 생성 시간

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
game_over = False  # 게임 오버 상태 추가
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if not game_over:  # 게임 오버가 아닐 때만 키 입력 처리
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # 적 생성 및 이동
        current_time = pygame.time.get_ticks()  # 현재 시간 가져오기
        if current_time - last_enemy_spawn_time > enemy_spawn_time:  # 일정 시간 경과 시
            spawn_enemy()
            last_enemy_spawn_time = current_time  # 마지막 적 생성 시간 업데이트

        for enemy in enemy_list:
            # 적이 플레이어를 향해 이동
            direction = [player_pos[0] - enemy[0], player_pos[1] - enemy[1]]
            distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            direction = [direction[0] / distance, direction[1] / distance]
            enemy[0] += direction[0] * enemy_speed
            enemy[1] += direction[1] * enemy_speed

            # 충돌 판정
            if detect_collision(player_pos, enemy):
                game_over = True  # 게임 오버 상태로 변경
                break  # 충돌 시 루프 종료

    # 화면 그리기
    screen.fill(WHITE)
    if game_over:  # 게임 오버 상태일 때
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
        
        # r 또는 q 버튼 입력 처리
        if keys[pygame.K_r]:  # r 버튼으로 재시작
            player_pos = [WIDTH // 2, HEIGHT // 2]
            enemy_list.clear()  # 적 리스트 초기화
            score = 0  # 점수 초기화
            game_over = False  # 게임 오버 상태 초기화
        elif keys[pygame.K_q]:  # q 버튼으로 종료
            running = False  # 게임 종료
    else:
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
    if not game_over:  # 게임 오버가 아닐 때만 점수 증가
        score += 1

# 게임 종료
pygame.quit()
