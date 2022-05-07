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

background = pygame.image.load(os.path.join(image_path, "background.jpg"))

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
weapon_speed = 6

ball_images = [
    pygame.image.load(os.path.join(image_path, f"balloon{i}.png")) for i in range(1, 5)
]

ball_speed_y = [-18, -15, -12, -9]  # balloon 1, 2, 3, 4의 최초 스피드

# 일단 가장 큰 공(balloon 1)에 대한 정보를 딕셔너리 원소로 초기화
balls = [
    {
        "x_pos": 50,  # 공의 x 좌표
        "y_pos": 50,  # 공의 y 좌표
        "image_index": 0,  # balloon 번호
        "to_x": 3,  # 공의 x축 이동
        "to_y": -7,  # 공의 y축 이동
        "init_speed_y": ball_speed_y[0],  # y축 이동 최초 속도
    }
]

# 사라질 무기, 공 정보 저장
weapon_to_remove = -1
ball_to_remove = -1

# 폰트 및 플레이 시간
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()

# 게임 종료 메시지 : Game Over, Time Over, Mission Complete
game_result = "Game Over"

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
                if len(weapons) < 3:  # 무기 개수 3개로 제한
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
        ball_x_pos = ball["x_pos"]
        ball_y_pos = ball["y_pos"]
        ball_image_index = ball["image_index"]

        ball_size = ball_images[ball_image_index].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 공이 벽과 바닥에 닿으면 방향을 반대로 전환
        if ball_x_pos < 0 or ball_x_pos > screen_width - ball_width:
            ball["to_x"] *= -1
        if ball_y_pos >= screen_height - stage_height - ball_height:
            ball["to_y"] = ball["init_speed_y"]
        else:
            ball["to_y"] += 0.4  # 위로 진행할 때는 속도를 줄이고, 아래로 진행할 때는 속도를 늘림 (포물선 효과)

        ball["x_pos"] += ball["to_x"]
        ball["y_pos"] += ball["to_y"]

    # 4. 충돌 처리
    # 캐릭터 위치 정보 저장
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 공 위치 정보 저장 + 충돌 처리
    for ball_index, ball in enumerate(balls):
        ball_x_pos = ball["x_pos"]
        ball_y_pos = ball["y_pos"]
        ball_image_index = ball["image_index"]

        ball_rect = ball_images[ball_image_index].get_rect()
        ball_rect.left = ball_x_pos
        ball_rect.top = ball_y_pos

        # 하나의 공이라도 닿으면 게임 종료 (실패)
        if character_rect.colliderect(ball_rect):
            is_playing = False
            break

        # 공과 무기의 충돌
        for weapon_index, weapon_value in enumerate(weapons):
            weapon_x_pos, weapon_y_pos = weapon_value
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos

            # 무기와 공이 충돌하면 공이 분리됨
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_index  # 무기 제거
                ball_to_remove = ball_index  # 공 제거

                if ball_image_index < 3:  # 가장 작은 공이 아니면 2개로 나누어짐
                    # 현재 공 크기 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_image_index + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 나누어지는 공
                    balls.append(
                        {
                            "x_pos": ball_x_pos
                            + (ball_width / 2)
                            - (small_ball_width / 2),
                            "y_pos": ball_y_pos
                            + (ball_height / 2)
                            - (small_ball_height / 2),
                            "image_index": ball_image_index + 1,
                            "to_x": -3,
                            "to_y": -7,
                            "init_speed_y": ball_speed_y[ball_image_index + 1],
                        }
                    )

                    # 오른쪽으로 나누어지는 공
                    balls.append(
                        {
                            "x_pos": ball_x_pos
                            + (ball_width / 2)
                            - (small_ball_width / 2),
                            "y_pos": ball_y_pos
                            + (ball_height / 2)
                            - (small_ball_height / 2),
                            "image_index": ball_image_index + 1,
                            "to_x": 3,
                            "to_y": -7,
                            "init_speed_y": ball_speed_y[ball_image_index + 1],
                        }
                    )

                break
        else:
            continue
        break

    # 충돌된 무기와 공 제거
    if weapon_to_remove > -1:
        weapons.pop(weapon_to_remove)
        weapon_to_remove = -1
    if ball_to_remove > -1:
        balls.pop(ball_to_remove)
        ball_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료 (성공)
    if not balls:
        game_result = "Mission Complete"
        is_playing = False

    # 5. 화면에 그리기 (작성 순서에 따라 우선 순위 바뀜)
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for ball in balls:
        ball_x_pos = ball["x_pos"]
        ball_y_pos = ball["y_pos"]
        ball_image_index = ball["image_index"]
        screen.blit(ball_images[ball_image_index], (ball_x_pos, ball_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(f"Time: {int(total_time - elapsed_time)}", True, (0, 0, 0))
    screen.blit(timer, (10, 10))

    # 시간 초과 (실패)
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        is_playing = False

    pygame.display.update()

# 게임 종료 메시지 띄우기
message = game_font.render(game_result, True, (255, 0, 0))
message_rect = message.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(message, (message_rect))
pygame.display.update()

pygame.time.delay(2000)  # 2초 대기 후 종료

# 게임 종료
pygame.quit()
