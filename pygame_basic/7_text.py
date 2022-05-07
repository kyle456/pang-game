import pygame

pygame.init()  # Pygame 초기화 (반드시 필요)

# 화면 크기 설정 (가로 x 세로)
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 제목 설정
pygame.display.set_caption("Kyle's Game")

# FPS (Frame per Second)
clock = pygame.time.Clock()

# 배경 이미지 설정
background = pygame.image.load("pygame_basic/background.png")

# 내 캐릭터
character = pygame.image.load("pygame_basic/character.png")
character_size = character.get_rect().size  # 캐릭터의 크기
character_width = character_size[0]  # 가로
character_height = character_size[1]  # 세로
character_x_pos = screen_width / 2 - character_width / 2  # 시작 x
character_y_pos = screen_height - character_height  # 시작 y

# 이동 관련
to_x, to_y = 0, 0
speed = 0.6

# 적 캐릭터
enemy = pygame.image.load("pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = screen_width / 2 - enemy_width / 2
enemy_y_pos = screen_height / 2 - enemy_height / 2

# 폰트 설정
game_font = pygame.font.Font(None, 40)  # 폰트, 크기

# 총 시간
total_time = 10

# 시작 시간
start_ticks = pygame.time.get_ticks()  # 시작 tick


# event loop (게임 플레이)
is_playing = True  # 게임이 진행 중인지 확인

while is_playing:
    delta = clock.tick(60)  # 게임 화면의 초당 프레임 수

    # 이벤트 발생
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 게임창이 닫히면
            is_playing = False

        if event.type == pygame.KEYDOWN:  # 키보드를 누르면
            if event.key == pygame.K_LEFT:
                to_x -= speed
            elif event.key == pygame.K_RIGHT:
                to_x += speed
            elif event.key == pygame.K_UP:
                to_y -= speed
            elif event.key == pygame.K_DOWN:
                to_y += speed

        if event.type == pygame.KEYUP:  # 키보드를 떼면
            if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                to_x = 0
            elif event.key in {pygame.K_UP, pygame.K_DOWN}:
                to_y = 0

    # 캐릭터 이동 (FPS에 따른 속도 보정)
    character_x_pos += to_x * delta
    character_y_pos += to_y * delta

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 충돌 처리를 위한 캐릭터 위치 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 적과 충돌 시 게임 종료
    if character_rect.colliderect(enemy_rect):
        print("충돌!")
        is_playing = False

    screen.blit(background, (0, 0))  # 배경, 시작 좌표
    # screen.fill((0, 0, 255))  # RGB 배경 설정

    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터, 시작 좌표
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))  # 적, 시작 좌표

    # 타이머
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # 경과시간(초)
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))  # 타이머, 시작 좌표

    if total_time - elapsed_time < 0:  # 시간이 모두 경과하면
        is_playing = False

    pygame.display.update()  # 게임 화면 다시 그리기

# 종료 전 2초 대기
pygame.time.delay(2000)

# 게임 종료
pygame.quit()
