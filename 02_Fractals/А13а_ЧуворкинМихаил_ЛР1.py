# 50 variant Chain

import numpy as np
from pyglet.gl import *
from pyglet.window import Window
from pyglet import app
import random

# 50 var - Chain
transform = np.array([
    [-0.75, -0.4, 0.4, -0.75, 0.00, 0.0],
    [0.09, -0.4, 0.4, 0.09, 0.91, -0.4]
])


# weights lists
list_w = [0.79, 0.21]

# width
w = 600
# start point
startX = random.randint(0, w-1)
startY = random.randint(0, w-1)

def getNewXY(startX, startY):
    '''Получает координаты для новой точки'''
    choice = random.choices(transform, weights=list_w)
    xx, xy, yx, yy, bx, by = choice[0] # unpack
    oldX, oldY = startX, startY
    startX = xx * oldX + xy * oldY + bx # new x coord
    startY = yx * oldX + yy * oldY + by # new y coord
    return (startX, startY)


# определяем начальную точку и ищем границы фрактала
xList = []
yList = []
for i in range(1000):
    startX, startY = getNewXY(startX, startY)
    if(i > 800):
        xList.append(startX)
        yList.append(startY)
# print(max(xList), min(xList))
# print(max(yList), min(yList))


scale = 100 # масштаб
def update(dt):
    '''Обновление массива точек - ищем 10000 новых'''
    global startX
    global startY
    global scale
    for i in range(10000):
        # print(startX, startY)
        # если использовать поиск границ
        toff = 0.5 # не догадался до зависимости от границ фрактала 
        # start + toff должны быть в (-2, 2)
        x = int ((startX + toff) * w / 2)
        y = int ((startY + toff) * w / 2)
        # если использовать переменную масштаба
        # x = int(startX*scale)
        # y = int(startY*scale)
        # print(x, y)
        vp[x, y] = [0, 0, 0]
        startX, startY = getNewXY(startX, startY)


# заполняем белым все
vp = np.full((w, w, 3), 255, dtype = 'uint8')

window = Window(visible = True, width = w, height = w, caption = '50 - Chain', resizable = 1)


def clear_resize(dt):
    '''Очищаем окно и меняем масштаб (если его используем) а также очищаем наш массив с цветами'''
    window.clear()
    global scale
    scale += 20 
    global vp
    vp = np.full((w, w, 3), 255, dtype = 'uint8')


pyglet.clock.schedule_interval(update, 0.01) # добавляем точки
# pyglet.clock.schedule_interval(clear_resize, 5) # очищаем экран

@window.event
def on_draw():
    vpf = vp.flatten() # преобразуем в одномерный массив
    vpf = (GLubyte * (w * w * 3))(*vpf) # преобразуем в gl unsigned byte
    glDrawPixels(w, w, GL_RGB, GL_UNSIGNED_BYTE, vpf)
app.run()