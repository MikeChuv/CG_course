
import numpy as np
from pyglet.gl import *
from pyglet.window import Window
from pyglet import app
import random


# from sample
transform = np.array([
    [0.3, -0.3, 0.3, 0.3, 1, 1],
    [0.3, -0.3, 0.3, 0.3, 1, -1],
    [0.3, -0.3, 0.3, 0.3, -1, 1],
    [0.3, -0.3, 0.3, 0.3, -1, -1]
])

# weights list
list_w = [0.25, 0.25, 0.25, 0.25]

# width
w = 600
startX = random.randint(0, w-1)
startY = random.randint(0, w-1)

def getNewXY(startX, startY):
    choice = random.choices(transform, weights=list_w)
    xx, xy, yx, yy, bx, by = choice[0] # unpack
    oldX, oldY = startX, startY
    startX = xx * oldX + xy * oldY + bx # new x coord
    startY = yx * oldX + yy * oldY + by # new y coord
    return (startX, startY)


xList = []
yList = []
for i in range(1000):
    startX, startY = getNewXY(startX, startY)
    if(i > 500):
        xList.append(startX)
        yList.append(startY)
# скоммуниздил у Ромы, типа ищем границы фрактала
print(max(xList), min(xList))
print(max(yList), min(yList))


scale = 100 # масштаб
def update(dt):
    global startX
    global startY
    global scale
    for i in range(10000):
        # print(startX, startY)
        # если использовать поиск границ
        toff = 0.0 # чета влом придумывать зависимость
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

window = Window(visible = True, width = w, height = w, caption = 'Sample', resizable = 1)


def clear_resize(dt):
    '''Очищаем окно и меняем масштаб (если его используем) а также очищаем наш массив с цветами'''
    window.clear()
    global scale
    scale += 20 
    global vp
    vp = np.full((w, w, 3), 255, dtype = 'uint8')


pyglet.clock.schedule_interval(update, 0.01) # 100 раз в секунду (я пытался) добавляем точки
# pyglet.clock.schedule_interval(clear_resize, 5) # раз в 5 секунд очищаем экран (если юзаете масштаб)

@window.event
def on_draw():
    vpf = vp.flatten() # преобразуем в одномерный массив
    vpf = (GLubyte * (w * w * 3))(*vpf) # преобразуем в gl unsigned byte
    glDrawPixels(w, w, GL_RGB, GL_UNSIGNED_BYTE, vpf)
app.run()