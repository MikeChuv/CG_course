from pyglet.gl import *
import pyglet
from pyglet import app, graphics
from pyglet.window import Window, key
import numpy as np
from sys import exit



rot_x = rot_y = rot_z = 0
# Вращение
n_rot, da = 0, 5
#

R = 30 # Радиус окружности (для построения треугольника)
h = R // 5 # Половина длины ребра куба
w = R + 2 * h # Для задания области вывода
width = height = 400 # Размер окна вывода
# Координаты вершин треугольника
ang = np.pi / 6
v0 = (-R * np.cos(ang), -R * np.sin(ang), 0)
v1 = (-v0[0], v0[1], 0)
v2 = (0, R, 0)

# Кубик
verts = ((h, -h, -h), # Координаты вершин куба
         (h, h, -h),
         (-h, h, -h),
         (-h, -h, -h),
         (h, -h, h),
         (h, h, h),
         (-h, -h, h),
         (-h, h, h))

faces = ((0, 1, 2, 3), # Индексы вершин граней куба
         (3, 2, 7, 6),
         (6, 7, 5, 4),
         (4, 5, 1, 0),
         (1, 5, 7, 2),
         (4, 0, 3, 6))


clrs = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0),
        (0, 1, 1), (1, 1, 1), (1, 0, 0), (0, 1, 0),
        (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 1, 1))


def generate_isoplane():
    sf = np.sqrt(1 / 3)
    cf = np.sqrt(2 / 3)
    sp = np.sqrt(1 / 2)
    cp = np.sqrt(1 / 2)
    isoplane = np.array([[cp, sf * sp, 0, 0],
                         [0, cp, 0, 0],
                         [sp, -sf * cp, 0, 0],
                         [0, 0, 0, 1]])
    isoplane = isoplane.flatten()
    isoplane = (GLfloat * 16)(*isoplane)
    return isoplane



def t_draw():
    glLineWidth(6)
    graphics.draw(3, GL_LINE_LOOP, ('v3f', v0 + v1 + v2), ('c3f', [1, 0, 0]*3))



def cube_draw():
    k = -1
    for face in faces:
        k += 1
        m = -1
        v4, c4 = (), ()
        for v in face:
            m += 1
            v4 += verts[v]
            c4 += clrs[k + m]
        graphics.draw(4, GL_QUADS, ('v3f', v4), ('c3f', c4))

def isoProjection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    isoplane = generate_isoplane()
    glLoadMatrixf(isoplane)
    glOrtho(-w, w, -w, w, -w, w)

def rotate(x, y, z):
    glRotatef(x, 1, 0, 0)
    glRotatef(y, 0, 1, 0)
    glRotatef(z, 0, 0, 1)

def place_cubes(vlist):
    for vertex in vlist:
        glPushMatrix()
        glTranslatef(*vertex)
        rotate(n_rot, n_rot, n_rot)
        cube_draw()
        glPopMatrix()


window = Window(visible = True, width = width, height = height, resizable = True)
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)


def update(dt):
    global rot_z, n_rot
    rot_z += 1
    #n_rot += 1

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    rotate(rot_x, rot_y, rot_z)
    t_draw()
    place_cubes([v0, v1, v2])
    isoProjection()

app.run()
