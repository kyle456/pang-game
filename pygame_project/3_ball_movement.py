"""
추억의 오락실 게임 - Pang Game 만들어보기 프로젝트
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

character_to_x = 0
character_speed = 5

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []  # 무기는 여러 개 사용 가능
weapon_speed = 10

ball_images = [
    pygame.image.load(os.path.join(image_path, f"balloon{i}.png")) for i in range(1, 5)
]

ball_speed_y = [-18, -15, -12, -9]  # balloon 1, 2, 3, 4의 최초 스피드

# 일단 가장 큰 공(balloon 1)에 대한 정보를 딕셔너리 원소로 초기화
balls = [
    {
        "pos_x": 50,  # 공의 x 좌표
        "pos_y": 50,  # 공의 y 좌표
        "image_index": 0,  # balloon 번호
        "to_x": 3,  # 공의 x축 이동
        "to_y": -6,  # 공의 y축 이동
        "init_speed_y": ball_speed_y[0],  # y축 이동 최초 속도
    }
]

is_playing = True

while is_playing:
    delta = clock.tick(60)

    # 2. 이벤트 처리 (키보드 ,마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 게임창이 닫히면
            is_playing = False

        if event.type == pygame.KEYDOWN:  # 키보드를 누르면
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = (
                    character_x_pos + (character_width / 2) - (weapon_width / 2)
                )  # 캐릭터의 중앙
                weapon_y_pos = character_y_pos  # 캐릭터의 가장 위
                weapons.append((weapon_x_pos, weapon_y_pos))

        if event.type == pygame.KEYUP:  # 키보드를 떼면
            if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                character_to_x = 0

    # 3. 캐릭터, 무기 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위로 발사(위치 계속 변경), 천장에 닿은 무기 없애기
    weapons = [
        (weapon_x_pos, weapon_y_pos - weapon_speed)
        for weapon_x_pos, weapon_y_pos in weapons
        if weapon_y_pos > 0
    ]

    for index, ball in enumerate(balls):
        ball_pos_x = ball["pos_x"]
        ball_pos_y = ball["pos_y"]
        ball_image_index = ball["image_index"]

        ball_size = ball_images[ball_image_index].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 공이 벽과 바닥에 닿으면 방향을 반대로 전환
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball["to_x"] *= -1
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball["to_y"] = ball["init_speed_y"]
        else:
            ball["to_y"] += 0.5  # 위로 진행할 때는 속도를 줄이고, 아래로 진행할 때는 속도를 늘림 (포물선 효과)

        ball["pos_x"] += ball["to_x"]
        ball["pos_y"] += ball["to_y"]

    # 4. 충돌 처리

    # 5. 화면에 그리기 (작성 순서에 따라 우선 순위 바뀜)
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for index, ball in enumerate(balls):
        ball_pos_x = ball["pos_x"]
        ball_pos_y = ball["pos_y"]
        ball_image_index = ball["image_index"]
        screen.blit(ball_images[ball_image_index], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()

# 게임 종료
pygame.quit()
