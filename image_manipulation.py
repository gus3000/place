from typing import List

import numpy as np
import png


def save_image(name: str, image: np.array, palette: List[List[int]]) -> None:
    w = png.Writer(len(image[0]), len(image), palette=palette, bitdepth=8)
    with open(name, 'wb') as f:
        w.write(f, image)


def hex_to_np(color: str):
    c = [int(color[2 * i:2 * i + 2], 16) for i in range(3)]
    # c.append(255)
    return c