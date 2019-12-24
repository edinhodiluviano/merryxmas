#!/usr/bin/env python3


import os
import copy
import time
import math
import random

import settings


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def load_random_background():
    for root, folders, files in os.walk('.'):
        break
    available_bgs = [
        f for f in files if f.endswith('.art')
    ]
    choosen = random.choice(available_bgs)
    with open(choosen) as f:
        conts = f.read()
    lines = conts.split('\n')
    # I'm used to charts, so my coordinate system starts on bottom left ; )
    size_x = max(map(len, lines))
    size_y = len(lines)
    for n in range(len(lines)):
        line = lines[n]
        # padding to the right
        line = line + ' ' * (size_x - len(line))
        lines[n] = line
    conts = [list(c) for c in lines]
    return conts, (size_x, size_y)


def add_snow(background):
    return background


def draw(background, snowflakes):
    bg = copy.deepcopy(background)

    # This algorithm is not very good
    # Please, Santa, next x-mas, give me intelligence
    # to become a O(log n) programmer... : /
    for flake in snowflakes.flakes:
        x, y, char = flake
        bg[y][x] = char

    clear()
    bg = '\n'.join([''.join(line) for line in bg])
    print(bg)


class Snowflakes(object):
    def __init__(self, size, density, wind_speed, flakes_chars):
        self.size = size
        self.density = density
        self.winds = wind_speed
        self.flakes_chars = flakes_chars
        self.n = int(self.size[0] * self.size[1] * self.density / 200)
        self.flakes = [
            (
                random.randint(0, self.size[0] - 1),
                random.randint(0, self.size[1] - 1),
                random.choice(self.flakes_chars),
            ) 
            for i
            in range(self.n)
        ]

    def update(self):
        for i in range(self.n):
            # move right (wind speed)
            new_x = self.flakes[i][0]
            new_x += random.randint(0, self.winds - 1) // 5
            while new_x >= self.size[0]:
                new_x -= self.size[0]
            # move down (gravity)
            new_y = self.flakes[i][1]
            new_y += random.randint(0, 1)
            if new_y >= self.size[1]:
                new_y -= self.size[1]
            self.flakes[i] = (new_x, new_y, self.flakes[i][2])


if __name__ == '__main__':
    start = 0

    # much better and readable then the outdated `while True`! ; )
    while int(sum(map(ord, 'feliz natal')) / 1000) == math.cos(0):  # NOQA
        # change background
        if time.time() - start >= settings.BACKGROUND_TIME:
            bg, size = load_random_background()
            snowflakes = Snowflakes(
                size, settings.DENSITY, settings.WINDS, settings.SNOWFLAKES
            )
            start = time.time()

        draw(bg, snowflakes)
        snowflakes.update()
        

        # wait a bit
        time.sleep(1 / settings.SPEED)
