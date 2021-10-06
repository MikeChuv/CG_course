import pyglet
from pyglet.gl import *
from pyglet.window import key
import numpy as np

window = pyglet.window.Window(width=720, height=480)
ar = 720 / 480
#window.projection = pyglet.window.Projection3D()
batch = pyglet.graphics.Batch()

mtClr0 = [1, 0, 1, 0] # Цвет материала
light_position0 = [0, 40, 40, 0] # Позиция источника света
lghtClr0 = [0.75, 0, 0, 0] # Цвет источника света

mtClr = (gl.GLfloat * 4)(*mtClr0)
light_position = (gl.GLfloat * 4)(*light_position0)
lghtClr = (gl.GLfloat * 4)(*lghtClr0)


tz = 0.5
n = 6
show_lids = True
show_normals = False
depth_test = True

def ngon(r, n, zv, di):
    l = []
    nl = []
    if di == 1:
        start, stop, step = 0, n, 1
    else:
        start, stop, step = n, 0, -1
    for i in range(start, stop, step):
        x = r * np.cos(2 * np.pi * i / n)
        y = r * np.sin(2 * np.pi * i / n)
        nx = np.cos(2 * np.pi * i / n)
        ny = np.sin(2 * np.pi * i / n)
        l.append([x, y, zv])
        nl.append([nx, ny, 0])
    return l, nl

lid_top, n_top = ngon(35, n, 40, -1)
lid_top_fl = tuple(sum(lid_top, []))
lid_bottom, n_bottom = ngon(35, n, 0, 1)
lid_bottom_fl = tuple(sum(lid_bottom, []))


def draw_lids():
    glBegin(GL_POLYGON)
    for v in lid_top:
        glColor3f(0, 0, 1)
        glNormal3f(0, 0, 1)
        glVertex3f(*v)
    glEnd()
    glBegin(GL_POLYGON)
    for v in lid_bottom:
        glColor3f(0, 0, 1)
        glNormal3f(0, 0, -1)
        glVertex3f(*v)
    glEnd()

def faces(n):
    for i in range(n):
        svl = (lid_bottom[i] , lid_bottom[(i+1)%n] , lid_top[n-1-i] , lid_top[(n-i)%n])
        snl = (n_bottom[i] , n_bottom[(i+1)%n] , n_top[n-1-i] , n_top[(n-i)%n])
        glBegin(GL_QUADS)
        for i, v in enumerate(svl):
            glColor3f(1, 0, 0)
            glNormal3f(*snl[i])
            glVertex3f(*v)
        glEnd()

def draw_normals(n):
    glLineWidth(3)
    for i in range(n):
        vn = np.array(n_top[i]) * 10 + np.array(lid_top[i])
        vl = list(vn) + lid_top[i]
        pyglet.graphics.draw(2, GL_LINES, ('v3f', vl ), ('c3f', [1, 1, 0] * 2))
    for i in range(n):
        vn = np.array(n_bottom[i]) * 10 + np.array(lid_bottom[i])
        vl = list(vn) + lid_bottom[i]
        pyglet.graphics.draw(2, GL_LINES, ('v3f', vl ), ('c3f', [1, 1, 0] * 2))

@window.event
def on_draw():
    window.clear()
    glEnable(GL_DEPTH_TEST) if depth_test else glDisable(GL_DEPTH_TEST)
    if show_lids: draw_lids()
    if show_normals: draw_normals(n)
    faces(n)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    w = 80
    glOrtho(-w, w, -w, w, -w, w)
    #gluPerspective(90, ar, .1, 1000)
    glMatrixMode(GL_MODELVIEW)
    #print(vlist[0:6], vlist[-3:], vlist[-6:-3])
    #batch.draw()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if modifiers & key.MOD_SHIFT:
        glRotatef(1, dx, dy, 0)
    else:
        glTranslatef(dx / 10, dy / 10, 0)


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    glTranslatef(0, 0, scroll_y * 5)



@window.event
def on_key_press(symbol, modifiers):
    global tz, show_lids, show_normals, depth_test
    if symbol == key._1:
        tz = 1
    if symbol == key._2:
        show_lids = not show_lids
    if symbol == key._3:
        glShadeModel(GL_FLAT)
    if symbol == key._4:
        glDisable(GL_LIGHTING)
    if symbol == key._5:
        show_normals = not show_normals
    if symbol == key._6:
        depth_test = not depth_test
    if symbol == key._7:
        glEnable(GL_CULL_FACE)

@window.event
def on_key_release(symbol, modifiers):
    global tz
    if symbol == key._1:
        tz = 0
    if symbol == key._3:
        glShadeModel(GL_SMOOTH)
    if symbol == key._4:
        glEnable(GL_LIGHTING)
    if symbol == key._7:
        glDisable(GL_CULL_FACE)

def rotate(dt):
    global tz
    glRotatef(0.5, tz / 20, 0, 0)
    #glRotatef(0.5, 0, dt, 0)
    #glRotatef(0.5, 0, 0, dt)
    #tz = 0


if __name__ == "__main__":
    glEnable(GL_MULTISAMPLE_ARB)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS) # GL_LESS GL_GREATER

    glEnable(GL_LIGHTING)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mtClr)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lghtClr)
    glEnable(GL_LIGHT0)

    model = pyglet.model.load("nprism2.obj", batch=batch)
    glEnable(GL_NORMALIZE)
    #glTranslatef(0, 0, 20)

    pyglet.clock.schedule_interval(rotate, 1/60)
    pyglet.app.run()
