import pygame

pygame.init()  # Pygame 초기화 (반드시 필요)

# 화면 크기 설정 (가로 x 세로)
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 제목 설정
pygame.display.set_caption("Kyle's Game")

# 배경 이미지 설정
background = pygame.image.load("pygame_basic/background.png")

# Sprite(== Character) 불러오기
character = pygame.image.load("pygame_basic/character.png")
character_size = character.get_rect().size  # 캐릭터의 크기
character_width = character_size[0]  # 가로
character_height = character_size[1]  # 세로
character_x_pos = screen_width / 2 - character_width / 2  # 시작 x
character_y_pos = screen_height - character_height  # 시작 y

# event loop (게임 플레이)
is_playing = True  # 게임이 진행 중인지 확인

while is_playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 게임창이 닫히면
            is_playing = False

    screen.blit(background, (0, 0))  # 배경, 시작 좌표
    # screen.fill((0, 0, 255))  # RGB 배경 설정

    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터, 시작 좌표

    pygame.display.update()  # 게임 화면 다시 그리기

# 게임 종료
pygame.quit()
