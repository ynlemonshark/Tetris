import pygame
import sys
from pygame.locals import QUIT, Rect
from random import randint

Display_width = 800
Display_height = 800

Surface_width = 800
Surface_height = 800

display_ratio_x = Display_width / Surface_width
display_ratio_y = Display_height / Surface_height

FPS = 40

pygame.init()
DISPLAY = pygame.display.set_mode((Display_width, Display_height))
SURFACE = pygame.Surface((Surface_width, Surface_height))
FPSCLOCK = pygame.time.Clock()


block_size = (45, 45)
block_colors = 7

block_image = pygame.transform.scale(pygame.image.load("resources/blocks.png"), (block_size[0] * (block_colors + 1),
                                                                                 block_size[1]))
tetrominoes_x = []
tetrominoes_y = []
tetrominoes_colors = []

file = open("resources/blocks.txt", 'r')

while True:
    line = file.readline()
    line = line.replace("\n", "")

    if line == "~":
        break

    else:
        line = line.split("/")

        tetrominoes_colors.append(int(line[0]))

        line[1] = line[1].split(",")
        x_to_append = []
        y_to_append = []

        x_to_append2 = []
        y_to_append2 = []
        for data in line[1]:
            extra = data
            extra = extra.split(":")

            x_to_append2.append(int(extra[0]))
            y_to_append2.append(int(extra[1]))
        x_to_append.append(x_to_append2)
        y_to_append.append(y_to_append2)

        middle_distance_x = max(x_to_append2)
        middle_distance_y = max(y_to_append2)

        x_to_append2 = []
        y_to_append2 = []
        for data in line[1]:
            extra = data
            extra = extra.split(":")
            x_to_append2.append(int(extra[1]))
            y_to_append2.append(-int(extra[0]) + middle_distance_x)
        x_to_append.append(x_to_append2)
        y_to_append.append(y_to_append2)

        x_to_append2 = []
        y_to_append2 = []
        for data in line[1]:
            extra = data
            extra = extra.split(":")
            x_to_append2.append(-int(extra[0]) + middle_distance_x)
            y_to_append2.append(-int(extra[1]) + middle_distance_y)
        x_to_append.append(x_to_append2)
        y_to_append.append(y_to_append2)

        x_to_append2 = []
        y_to_append2 = []
        for data in line[1]:
            extra = data
            extra = extra.split(":")
            x_to_append2.append(-int(extra[1]) + middle_distance_y)
            y_to_append2.append(int(extra[0]))
        x_to_append.append(x_to_append2)
        y_to_append.append(y_to_append2)

        tetrominoes_x.append(x_to_append)
        tetrominoes_y.append(y_to_append)

file.close()

field_frame_rect = Rect(40, 40, 470, 695)
field_frame_image = pygame.transform.scale(pygame.image.load("resources/field_frame.png"), field_frame_rect.size)

field_x_range = 10
field_y_range = 15

field_topleft = (50, 50)

falling_speed = 500

DAS = 500
ARR = 50

down_ARR = 50

generation_pos = (4, 0)


def collidefield(field, tetromino, rotation, position, move_x, move_y):
    if 0 <= position[0] + move_x and\
       0 <= position[1] + move_y and\
       field_x_range > position[0] + max(tetrominoes_x[tetromino][rotation]) + move_x and\
       field_y_range > position[1] + max(tetrominoes_y[tetromino][rotation]) + move_y:

        all_true = True
        for index in range(len(tetrominoes_x[tetromino][rotation])):
            if field[tetrominoes_y[tetromino][rotation][index] + position[1] + move_y]\
                    [tetrominoes_x[tetromino][rotation][index] + position[0] + move_x]:
                all_true = False

        if all_true:
            return True
        else:
            return False

    else:
        return False


def main():
    FLAG = 1

    FIELD = []
    for y in range(field_y_range):
        to_append = []
        for x in range(field_x_range):
            to_append.append(0)
        FIELD.append(to_append)

    FALLING = randint(0, len(tetrominoes_x) - 1)
    FALLING_POSITION = [generation_pos[0], generation_pos[1]]
    FALLING_DELAY = 0
    FALLING_ROTATION = 0

    press_left = -DAS
    pressing_left = False
    press_right = -DAS
    pressing_right = False

    press_down = 0
    pressing_down = False



    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif pygame_event.type == pygame.KEYDOWN:
                if FLAG == 1:
                    if pygame_event.key == pygame.K_LEFT:
                        if collidefield(FIELD, FALLING, FALLING_ROTATION, FALLING_POSITION, -1, 0):
                            FALLING_POSITION[0] -= 1
                        pressing_left = True
                    elif pygame_event.key == pygame.K_RIGHT:
                        if collidefield(FIELD, FALLING, FALLING_ROTATION, FALLING_POSITION, 1, 0):
                            FALLING_POSITION[0] += 1
                        pressing_right = True

                    elif pygame_event.key == pygame.K_DOWN:
                        pressing_down = True

                    elif pygame_event.key == pygame.K_SPACE:
                        if collidefield(FIELD, FALLING, (FALLING_ROTATION + 1) % 4, FALLING_POSITION, 0, 0):
                            FALLING_ROTATION += 1
                            FALLING_ROTATION %= 4

            elif pygame_event.type == pygame.KEYUP:
                if pygame_event.key == pygame.K_LEFT:
                    pressing_left = False
                    press_left = -DAS
                if pygame_event.key == pygame.K_RIGHT:
                    pressing_right = False
                    press_right = -DAS
                if pygame_event.key == pygame.K_DOWN:
                    pressing_down = False
                    press_down = 0

        if FLAG == 1:
            FALLING_DELAY += 1000 / FPS

            if press_down >= down_ARR:
                for repeat in range(int(press_down / down_ARR)):
                    if collidefield(FIELD, FALLING, FALLING_ROTATION, FALLING_POSITION, 0, 1):
                        FALLING_POSITION[1] += 1
                        press_down -= down_ARR
                    else:
                        break

            if FALLING_DELAY // falling_speed:
                while FALLING_DELAY // falling_speed:
                    if collidefield(FIELD, FALLING, FALLING_ROTATION, FALLING_POSITION, 0, 1):
                        FALLING_DELAY -= falling_speed
                        FALLING_POSITION[1] += 1
                    else:
                        FALLING_DELAY = 0
                        for repeat in range(len(tetrominoes_x[FALLING][FALLING_ROTATION])):
                            FIELD[tetrominoes_y[FALLING][FALLING_ROTATION][repeat] + FALLING_POSITION[1]]\
                                [tetrominoes_x[FALLING][FALLING_ROTATION][repeat] + FALLING_POSITION[0]] = tetrominoes_colors[FALLING]

                        FALLING_POSITION = [generation_pos[0], generation_pos[1]]
                        FALLING_ROTATION = 0
                        FALLING = randint(0, len(tetrominoes_x) - 1)


            if pressing_left:
                press_left += 1000 / FPS
            if pressing_right:
                press_right += 1000 / FPS
            if pressing_down:
                press_down += 1000 / FPS

            if press_left >= ARR:
                if collidefield(FIELD, FALLING, FALLING_ROTATION, FALLING_POSITION, -int(press_left / ARR), 0):
                    FALLING_POSITION[0] -= int(press_left / ARR)
                press_left %= ARR
            if press_right >= ARR:
                if collidefield(FIELD, FALLING, FALLING_ROTATION, FALLING_POSITION, int(press_right / ARR), 0):
                    FALLING_POSITION[0] += int(press_right / ARR)
                press_right %= ARR

            for index in range(field_y_range):
                all_true = True
                for repeat in range(field_x_range):
                    all_true = all_true and FIELD[index][repeat]

                if all_true:
                    FIELD[index] = 0
            for repeat in range(FIELD.count(0)):
                FIELD.remove(0)

            for repeat in range(field_y_range - len(FIELD)):
                to_append = []
                for x in range(field_x_range):
                    to_append.append(0)
                FIELD.insert(0, to_append)

                print(len(FIELD))


        SURFACE.fill((255, 255, 255))

        SURFACE.blit(field_frame_image, field_frame_rect.topleft)

        for y in range(field_y_range):
            for x in range(field_x_range):
                SURFACE.blit(block_image, (field_topleft[0] + x * block_size[0], field_topleft[1] + y * block_size[1]),
                             (block_size[0] * FIELD[y][x], 0, block_size[0], block_size[1]))

        if FLAG == 1:
            for index in range(len(tetrominoes_x[FALLING][FALLING_ROTATION])):
                SURFACE.blit(block_image, (field_topleft[0] + (tetrominoes_x[FALLING][FALLING_ROTATION][index] + FALLING_POSITION[0]) * block_size[0],
                                           field_topleft[1] + (tetrominoes_y[FALLING][FALLING_ROTATION][index] + FALLING_POSITION[1]) * block_size[1]),
                             (tetrominoes_colors[FALLING] * block_size[0], 0, block_size[0], block_size[1]))

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
