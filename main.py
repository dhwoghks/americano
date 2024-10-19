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
player_health = 5
player_speed = 5

# 적 설정
enemy_size = 30
enemy_health = 3  # 적의 체력 추가
enemy_list = []
enemy_speed = 1.5

# 총알 설정
bullet_size = 5
bullet_speed = 10
bullets = []  # 총알 리스트 추가
bullet_cooldown = 100  # 총알 발사 쿨타임 (밀리초)
last_bullet_time = 0  # 마지막 총알 발사 시간 초기화

# 게임 변수
clock = pygame.time.Clock()
FPS = 60
score = 0
enemy_spawn_time = 1000  # 적 생성 간격 (밀리초)
last_enemy_spawn_time = pygame.time.get_ticks()  # 마지막 적 생성 시간

# 충돌 판정 함수 (적의 체력 감소)
def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos
    distance = math.sqrt((p_x - e_x) ** 2 + (p_y - e_y) ** 2)
    return distance < (player_size / 2 + enemy_size / 2)

# 적 생성 함수
def spawn_enemy():
    direction = random.choice(['left', 'right', 'top', 'bottom'])  # 생성 방향 선택

    if direction == 'left':
        x_pos = random.randint(-enemy_size, 0)  # 왼쪽 바깥에서 생성
        y_pos = random.randint(0, HEIGHT)  # y 위치는 화면 안에서 랜덤
    elif direction == 'right':
        x_pos = random.randint(WIDTH, WIDTH + enemy_size)  # 오른쪽 바깥에서 생성
        y_pos = random.randint(0, HEIGHT)  # y 위치는 화면 안에서 랜덤
    elif direction == 'top':
        x_pos = random.randint(0, WIDTH)  # x 위치는 화면 안에서 랜덤
        y_pos = random.randint(-enemy_size, 0)  # 위쪽 바깥에서 생성
    else:  # direction == 'bottom'
        x_pos = random.randint(0, WIDTH)  # x 위치는 화면 안에서 랜덤
        y_pos = random.randint(HEIGHT, HEIGHT + enemy_size)  # 아래쪽 바깥에서 생성

    enemy_list.append([x_pos, y_pos])  # 적의 위치 추가

# 총알 생성 함수
def spawn_bullet(player_pos, direction):
    bullet_pos = [player_pos[0], player_pos[1]]
    bullets.append((bullet_pos, direction))  # 방향도 함께 저장

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
        # 플레이어 이동 (WASD 키)
        if keys[pygame.K_w] and player_pos[1] > player_size // 2:  # 위쪽 경계 체크
            player_pos[1] -= player_speed
        if keys[pygame.K_s] and player_pos[1] < HEIGHT - player_size // 2:  # 아래쪽 경계 체크
            player_pos[1] += player_speed
        if keys[pygame.K_a] and player_pos[0] > player_size // 2:  # 왼쪽 경계 체크
            player_pos[0] -= player_speed
        if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size // 2:  # 오른쪽 경계 체크
            player_pos[0] += player_speed
        
        # 총알 발사 (방향키로 변경)
        direction = None
        if keys[pygame.K_UP]:  # 위 방향키
            direction = [0, -1]
        elif keys[pygame.K_DOWN]:  # 아래 방향키
            direction = [0, 1]
        elif keys[pygame.K_LEFT]:  # 왼쪽 방향키
            direction = [-1, 0]
        elif keys[pygame.K_RIGHT]:  # 오른쪽 방향키
            direction = [1, 0]

        if direction and (current_time - last_bullet_time > bullet_cooldown):  # 쿨타임 체크
            spawn_bullet(player_pos, direction)
            last_bullet_time = current_time  # 마지막 총알 발사 시간 업데이트

        # 총알 이동 및 충돌 처리
        for bullet in bullets[:]:
            bullet_pos, bullet_direction = bullet  # 총알 위치와 방향 분리
            bullet_pos[0] += bullet_direction[0] * bullet_speed  # 총알 이동 (x 방향)
            bullet_pos[1] += bullet_direction[1] * bullet_speed  # 총알 이동 (y 방향)
            if bullet_pos[1] < 0 or bullet_pos[1] > HEIGHT or bullet_pos[0] < 0 or bullet_pos[0] > WIDTH:  # 화면 밖으로 나가면 제거
                bullets.remove(bullet)
                continue

            for enemy in enemy_list[:]:
                if detect_collision(bullet_pos, enemy):  # 총알의 위치를 사용하도록 수정
                    enemy_health -= 1  # 적의 체력 감소
                    bullets.remove(bullet)  # 총알 제거
                    if enemy_health <= 0:  # 적의 체력이 0 이하일 경우
                        enemy_list.remove(enemy)  # 적 제거
                    break

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
                player_health -= 1  # 플레이어의 체력 감소
                enemy_list.remove(enemy)  # 적 제거
                if player_health <= 0:  # 플레이어의 체력이 0 이하일 경우
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
        
        # 재시작 및 종료 안내 문구 추가
        restart_text = pygame.font.Font(None, 36).render("Press R to Restart or Q to Quit", True, (0, 0, 0))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
        
        # r 또는 q 버튼 입력 처리
        if keys[pygame.K_r]:  # r 버튼으로 재시작
            player_pos = [WIDTH // 2, HEIGHT // 2]
            enemy_list.clear()  # 적 리스트 초기화
            score = 0  # 점수 초기화
            player_health = 5 # 체력 초기화
            game_over = False  # 게임 오버 상태 초기화
        elif keys[pygame.K_q]:  # q 버튼으로 종료
            running = False  # 게임 종료
    else:
        pygame.draw.circle(screen, GREEN, (player_pos[0], player_pos[1]), player_size // 2)
        for enemy in enemy_list:
            pygame.draw.circle(screen, RED, (int(enemy[0]), int(enemy[1])), enemy_size // 2)
            
        # 총알 그리기
        for bullet in bullets:
            pygame.draw.circle(screen, (0, 0, 255), (int(bullet[0][0]), int(bullet[0][1])), bullet_size)  # bullet[0]에서 x, y 좌표 분리

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
