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

# Sprite(== Character) 불러오기
character = pygame.image.load("pygame_basic/character.png")
character_size = character.get_rect().size  # 캐릭터의 크기
character_width = character_size[0]  # 가로
character_height = character_size[1]  # 세로
character_x_pos = screen_width / 2 - character_width / 2  # 시작 x
character_y_pos = screen_height - character_height  # 시작 y

# 이동 관련
to_x, to_y = 0, 0
speed = 0.6

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

    # 캐릭터 이동
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

    screen.blit(background, (0, 0))  # 배경, 시작 좌표
    # screen.fill((0, 0, 255))  # RGB 배경 설정

    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터, 시작 좌표

    pygame.display.update()  # 게임 화면 다시 그리기

# 게임 종료
pygame.quit()
