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

# event loop
is_playing = True  # 게임이 진행 중인지 확인

while is_playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 게임창이 닫히면
            is_playing = False

    screen.blit(background, (0, 0))  # 이미지, 시작 좌표
    # screen.fill((0, 0, 255))  # RGB 배경 설정

    pygame.display.update()  # 게임 화면 다시 그리기

# 게임 종료
pygame.quit()
