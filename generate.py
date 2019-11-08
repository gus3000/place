import csv
import time
from pprint import pprint
import numpy as np

from image_manipulation import save_image, hex_to_np

# MAX_TO_READ = 16567568
MAX_TO_READ = 100
STEP = 2 ** 18

start = time.time()
# index	color code
color_indices = {
    0: "FFFFFF",
    1: "E4E4E4",
    2: "888888",
    3: "222222",
    4: "FFA7D1",
    5: "E50000",
    6: "E59500",
    7: "A06A42",
    8: "E5D900",
    9: "94E044",
    10: "02BE01",
    11: "00E5F0",
    12: "0083C7",
    13: "0000EA",
    14: "E04AFF",
    15: "820080"
}

for i in range(len(color_indices)):
    color_indices[i] = hex_to_np(color_indices[i])
palette = list(color_indices.values())
# pprint(palette)

# canvas = []
# for i in range(1000):
#     row = []
#     for j in range(1000):
#         row.append(0)
#     canvas.append(row)
# canvas = np.zeros((1001, 1001), dtype=[('color', 'i8')])
canvas = [[0] * 1001 for j in range(1001)]

# pprint(canvas)
tiles = []
i = 0
inputs = {}
inputs_np = np.zeros(MAX_TO_READ, dtype=[('date', 'S23'), ('user', 'S24'), ('x', 'i2'), ('y', 'i2'), ('color', 'i1')])

# pprint(inputs_np)

with open('csv/place_tiles_shuffled', 'r') as f:
    tile_reader = csv.reader(f, delimiter=',')
    next(tile_reader)  # skip header row
    for line in tile_reader:
        i += 1
        if i >= MAX_TO_READ:
            break

        x: int
        y: int
        # noinspection PyRedeclaration
        date, user, x, y, color = line
        # print(date)
        try:
            x = int(x)
            y = int(y)
            color = int(color)
        #     date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f UTC")
        except ValueError:
            continue
        # line = [date, user, x, y, color]
        # inputs[date] = [user, x, y, color]
        inputs_np[i] = (date[6:], user, x, y, color)
        # print(line)
print(f"[{time.time() - start:0.4}] {i} lines read")
inputs_np.sort(0)
# inputs = OrderedDict(sorted(inputs.items()))
pprint(inputs_np)
print(f"[{time.time() - start:0.4}] sorted")
i = 0
nb_steps = 0
for elem in inputs_np:
    if i % STEP == 0:
        save_image(f"img/{nb_steps}.png", canvas, palette)
        nb_steps += 1
    date, user, x, y, c = elem
    canvas[y][x] = c
    i += 1
save_image(f"img/{nb_steps}.png", canvas, palette)

print(f"[{time.time() - start:0.4}] parsed")
# print(canvas[1])
