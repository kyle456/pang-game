"""
pygame을 통한 게임 만들기 뼈대
"""

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

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

is_playing = True

while is_playing:
    delta = clock.tick(60)

    # 2. 이벤트 처리 (키보드 ,마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 게임창이 닫히면
            is_playing = False

    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌 처리

    # 5. 화면에 그리기

    pygame.display.update()

# 게임 종료
pygame.quit()
