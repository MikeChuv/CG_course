from pyglet.gl import *
from pyglet import app
from pyglet.window import Window, key
import numpy as np
d = 12
wx, wy = 1.5 * d, 1.1 * d # Параметры области визуализации
width, height = int(40 * wx), int(40 * wy) # Размеры окна вывода
texFromFile = False # True False

if texFromFile:
    tile_x = 2 # Число повторов текстуры по X
    tile_y = 1 # Число повторов текстуры по Y
else:
    tile_x = tile_y = 1

def to_c_float_Array(data): # Преобразование в си-массив
    return (GLfloat * len(data))(*data)

vld = to_c_float_Array([-d/2, -d, d*2]) # Левая нижняя вершина
vrd = to_c_float_Array([d/2, -d, d*2]) # Правая нижняя вершина
vru = to_c_float_Array([d, d, 0]) # Правая верхняя вершина
vlu = to_c_float_Array([-d, d, 0]) # Левая верхняя вершина
#
def texInit():
    if texFromFile:
        fn = 'G:\\python\\openGL\\кот.jpg'
        img = pyglet.image.load(fn)
        iWidth = img.width
        iHeight = img.height
        img = img.get_data('RGB', iWidth * 3)
    else:
        iWidth = iHeight = 64 # Размер текстуры равен iWidth * iHeight
        n = 3 * iWidth * iHeight
        # Каждый элемент текстуры содержит три компонента (формат текстуры GL_RGB)
        # GL_UNSIGNED_BYTE - это диапазон 0-255, поэтому для img задается тип uint8, а затем GLubyte
        img = np.zeros((3, iWidth, iHeight), dtype = 'uint8')
        for i in range(iHeight): # Генерация черно-белого образа, на основе которого создается текстура
         for j in range(iWidth):
            img[:, i, j] = ((i - 1) & 16 ^ (j - 1) & 16) * 255
        img = img.reshape(n)
        img = (GLubyte * n)(*img)
    p = GL_TEXTURE_2D
    r = GL_RGB
    # Задаем параметры текстуры
    glTexParameterf(p, GL_TEXTURE_WRAP_S, GL_REPEAT) # GL_CLAMP
    glTexParameterf(p, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(p, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(p, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # Способ взаимодействия с текущим фрагментом изображения
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    # Создаем 2d-текстуру на основе образа img
    glTexImage2D(p, 0, r, iWidth, iHeight, 0, r, GL_UNSIGNED_BYTE, img)
    glEnable(p)

window = Window(visible = True, width = width, height = height,
                resizable = True, caption = 'Текстура')
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
texInit()

py = 0

def update(dt):
    global py
    if py == 360:
        py = 0
    else:
        py += 1

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-wx, wx, -wy, wy, -20, 20)
    glRotatef(py, 1, 0, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3fv(vld)
    glTexCoord2f(tile_x, 0)
    glVertex3fv(vrd)
    glTexCoord2f(tile_x, tile_y)
    glVertex3fv(vru)
    glTexCoord2f(0, tile_y)
    glVertex3fv(vlu)
    glEnd()
app.run()
