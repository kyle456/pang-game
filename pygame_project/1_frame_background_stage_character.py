"""
추억의 오락실 게임 - Pang 게임 만들어보기 프로젝트
"""

import os
import pygame

pygame.init()  # Pygame 초기화 (반드시 필요)

# 화면 크기 설정 (가로 x 세로)
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 제목 설정
pygame.display.set_caption("Pang Game")

# FPS (Frame per Second)
clock = pygame.time.Clock()

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)  # 현재 파일 위치
image_path = os.path.join(current_path, "images")  # images 폴더 위치 반환

background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지의 높이 위에 캐릭터 놓기 위함

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height - stage_height


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
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()

# 게임 종료
pygame.quit()
