from noise import pnoise2


def generate_height_map(dim: int,
                        octaves: int,
                        persistence: float,
                        repeatx: int,
                        repeaty: int) -> bytearray:
    hmap = bytearray([0 for _ in range(dim * dim)])
    for i in range(dim):
        for j in range(dim):
            n = pnoise2(i / 16,
                        j / 16,
                        octaves=octaves,
                        persistence=persistence,
                        repeatx=repeatx,
                        repeaty=repeaty)
            hmap[i * dim + j] = int((n + 1) * 128)
    return hmap
