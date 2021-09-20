# Лабораторная работа 2 
# Чуворкин Михаил А-13а-19

import math
from pyglet.gl import *
from pyglet import app, graphics
from pyglet.window import Window, key


# Окно вывода
w = 800
h = 600

window = Window(visible = True, width = w, height = h,
                resizable = True, caption = 'FRONT_BACK')

glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT) # заливка окна цветом фона
glLineWidth(8)
glPolygonMode(GL_FRONT, GL_FILL) # Заливка лицевой стороны
glPolygonMode(GL_BACK, GL_LINE) # Вывод нелицевой стороны в виде линий (ребер)
px = py = 0

# time = 0.0

# def update(dt):
#     global px, py, time
#     px = 3 * math.cos(time)
#     py = 3 * math.sin(time)
#     time += dt / 10


# pyglet.clock.schedule_interval(update, 1 / 60)


def rotate():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(180*px, 1, 0, 0) # Поворот вокруг оси X
    glRotatef(180*py, 0, 1, 0) # Поворот вокруг оси Y

# проецирование
def reshape():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-8, 8, -6, 6, -3, 3) # Прямоугольное проецирование
    # glFrustum(-4, 4, -3, 3, 1, 25)
    glMatrixMode(GL_MODELVIEW)

# фиолетовый полигон на фоне
def draw_polygon():
    glPointSize(16)
    glPolygonMode(GL_BACK, GL_POINT) # Вывод нелицевой стороны в виде линий (ребер)
    vP1 = 2
    glColor3f(0.4, 0.1, 0.4)
    glBegin(GL_POLYGON)
    glVertex3f(-vP1, -vP1, 0)
    glVertex3f(vP1, -vP1, 0)
    glVertex3f(vP1, vP1, 0)
    glVertex3f(-vP1, vP1, 0)
    glEnd()

# разноцветный четырехугольник из треугольников
def draw_triangles():
    glPolygonMode(GL_BACK, GL_LINE) # Вывод нелицевой стороны в виде линий (ребер)
    tvx, tvy = 3, 2
    vertex_list = graphics.vertex_list(4, 'v2f', 'c3f')
    vertex_list.vertices = [-tvx, tvy, 0, -tvy, 0, tvy*2, tvx, tvy]
    vertex_list.colors = [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0.7]
    vertex_list.draw(GL_TRIANGLE_STRIP)

# пунктирная линия
def draw_line():
    lV1 = 3
    glEnable(GL_LINE_STIPPLE)
    pattern = '0b1111100000011111' # '1111100110011111'
    glLineStipple(2, int(pattern, 2)) # Повторяем каждый бит образца 2 раза
    vertex_list = graphics.vertex_list(3, 'v2f', 'c3f')
    vertex_list.vertices = [-lV1, -lV1, 0, lV1, lV1, -lV1]
    vertex_list.colors = [1, 0.5, 0, 1, 0, 0.2, 0.3, 1, 0.5]
    vertex_list.draw(GL_LINE_LOOP)
    glDisable(GL_LINE_STIPPLE)

@window.event
def on_draw():
    window.clear()
    rotate()
    reshape()
    draw_polygon()
    draw_triangles()
    draw_line()

@window.event
def on_key_press(symbol, modifiers):
    global px, py
    if symbol == key._1:
        px = 1 - px
        py = 0
    elif symbol == key._2:
        px = 0
        py = 1 - py
    elif symbol == key._3:
        glShadeModel(GL_FLAT) # без интерполяции цветов
    elif symbol == key._4:
        glShadeModel(GL_SMOOTH) # с интерполяцией цветов
app.run()

