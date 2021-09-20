import numpy as np
from pyglet.gl import *
import random
from pyglet.window import Window
from pyglet import app

w = 700
vp = np.full((w, w, 3), 255, dtype='uint8')

weight_table = np.array([0.7, 0.3])  # веса

transform = np.array([[-0.75, -0.30, 0.30, -0.75, 0.0, 0.00],
                     [0.30, -0.35, 0.35, 0.30, 0.7, -0.35]])  # второе сиф-преобразование

x, y = [], []

# Поиск начальной точки
start_x, start_y = w / 2, w / 2
for i in range(1000):
    N = random.choices(transform, weight_table)
    xx, xy, yx, yy, bx, by = N[0]
    old_x, old_y = start_x, start_y
    start_x = old_x * xx + old_y * yy + bx
    start_y = old_x * yx + old_y * yy + by
    if i > 500:
        x.append(start_x)
        y.append(start_y)

print(max(x), ' + ', min(x))
print(max(y), ' + ', min(y))

for _ in range(50000):
    N = random.choices(transform, weight_table)
    xx, xy, yx, yy, bx, by = N[0]
    old_x, old_y = start_x, start_y
    start_x = old_x * xx + old_y * yy + bx
    start_y = old_x * yx + old_y * yy + by
    # vp[int(w/2 + start_x * w/3) % w, int(w/2 + start_y * w/3) % w] = [0, 0, 0]
    vp[int(((start_x + 1) / 2) * w)][int(((start_y + 1) / 2) * w)] = [0, 0, 0]

vp = vp.flatten()
vp = (GLubyte * (w * w * 3))(*vp)
window = Window(visible=True, width=w, height=w, caption='Chain_2')


@window.event
def on_draw():
    window.clear()
    glDrawPixels(w, w, GL_RGB, GL_UNSIGNED_BYTE, vp)

app.run()
