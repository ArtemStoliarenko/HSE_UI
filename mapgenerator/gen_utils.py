from noise import pnoise2
from random import randint

# TODO: add scale

SQRT_2 = 2 ** 0.5
HALF_SQRT_2 = SQRT_2 / 2
VARIANCE = 100


def _hex_to_rgb(hex_color: str) -> bytearray:
    assert len(hex_color) == 7
    res = bytearray(3)
    res[0] = int(hex_color[1:3], base=16)
    res[1] = int(hex_color[3:5], base=16)
    res[2] = int(hex_color[5:7], base=16)
    return res


def _height_to_color(colors: dict, value: float) -> bytearray:
    color = min(colors.keys(), key=lambda x: abs(colors[x] - value))
    return _hex_to_rgb(color)


def generate_colored_map(dim: int,
                         octaves: int,
                         persistence: float,
                         repeatx: int,
                         repeaty: int,
                         colors: dict) -> bytearray:
    hmap = bytearray([0 for _ in range(dim * dim * 3)])
    lin_idx = 0
    offset = randint(0, VARIANCE)
    magic_const = 0.6
    #
    # debug_min = 2
    # debug_max = -2
    #
    for i in range(dim):
        for j in range(dim):
            n = pnoise2(i / dim + offset,
                        j / dim + offset,
                        octaves=octaves,
                        persistence=persistence,
                        repeatx=repeatx,
                        repeaty=repeaty)
            normed_height = (n + magic_const) * magic_const
            # debug_max = max(normed_height, debug_max)
            # debug_min = min(normed_height, debug_min)
            lin_idx += 3
            rgb = _height_to_color(colors, normed_height)
            hmap[lin_idx: lin_idx + 3] = rgb
    # print(f"Max height: {debug_max}")
    # print(f"Min height: {debug_min}")
    return hmap


def generate_height_map(dim: int,
                        octaves: int,
                        persistence: float,
                        repeatx: int,
                        repeaty: int) -> bytearray:
    hmap = bytearray([0 for _ in range(dim * dim)])
    offset = randint(0, VARIANCE)
    for i in range(dim):
        for j in range(dim):
            n = pnoise2(i / dim + offset,
                        j / dim + offset,
                        octaves=octaves,
                        persistence=persistence,
                        repeatx=repeatx,
                        repeaty=repeaty)
            hmap[i * dim + j] = int((n + 1) * 128)
    return hmap
