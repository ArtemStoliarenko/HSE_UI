from noise import pnoise2
from random import randint

import numpy as np

# TODO: add scale

SQRT_2 = 2 ** 0.5
HALF_SQRT_2 = SQRT_2 / 2
VARIANCE = 1000


def hex_to_rgb(hex_color: str) -> bytearray:
    assert len(hex_color) == 7
    res = bytearray(3)
    res[0] = int(hex_color[1:3], base=16)
    res[1] = int(hex_color[3:5], base=16)
    res[2] = int(hex_color[5:7], base=16)
    return res


def _height_to_color(colors: dict, value: float) -> bytearray:
    color = min(colors.keys(), key=lambda x: abs(colors[x] - value))
    return hex_to_rgb(color)


def numpy_to_bytearray(arr: np.array) -> bytearray:
    res = bytearray(arr.tobytes())
    # print(f"Source shape: {arr.shape}")
    # print(f"Res len: {len(res)}")
    # print(f"Equals: {len(res) == arr.shape[0] * arr.shape[1] * arr.shape[2]}")
    return res


def numpy_to_bytes(arr: np.array) -> bytes:
    return arr.tobytes()


def colorize(hmap: np.array, colors: dict):
    sorted_colors = sorted(colors.keys(), key=lambda x: colors[x])
    col_hmap = np.zeros([*hmap.shape, 3], dtype="uint8")
    col_hmap[:] = hex_to_rgb(sorted_colors[0])
    for col in sorted_colors[1:]:
        col_hmap[hmap >= colors[col]] = np.array(hex_to_rgb(col))
    return col_hmap


def generate_colored_map(dim: int,
                         scale: float,
                         octaves: int,
                         persistence: float,
                         repeatx: int,
                         repeaty: int,
                         colors: dict) -> np.array:
    hmap = generate_height_map(dim=dim,
                               scale=scale,
                               octaves=octaves,
                               persistence=persistence,
                               repeatx=repeatx,
                               repeaty=repeaty)
    col_hmap = colorize(hmap, colors)
    return col_hmap


def generate_height_map(dim: int,
                        scale: float,
                        octaves: int,
                        persistence: float,
                        repeatx: int,
                        repeaty: int) -> np.array:
    hmap = np.zeros([dim, dim], dtype=float)
    offset = randint(0, VARIANCE)
    scale_coef = 0.5 / (dim * scale + 1)
    print(scale_coef)
    for i in range(dim):
        for j in range(dim):
            n = pnoise2(i * scale_coef + offset,
                        j * scale_coef + offset,
                        octaves=octaves,
                        persistence=persistence,
                        repeatx=repeatx,
                        repeaty=repeaty)
            hmap[i][j] = n
    # Norming
    min_h = np.min(hmap)
    hmap = hmap + abs(min_h)
    max_h = np.max(hmap)
    norm_coef = 1 / max_h
    hmap *= norm_coef
    ### DEBUG
    # print(f"New max: {np.max(hmap)}")
    # print(f"New min: {np.min(hmap)}")
    ###
    return hmap
