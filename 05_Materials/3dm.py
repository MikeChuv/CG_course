import pyglet
from pyglet.gl import *
from pyglet.window import key
import numpy as np

window = pyglet.window.Window(width=720, height=480)
ar = 720 / 480

time = 0.0

mtClr0 = [1, 1, 1, 1] # Цвет материала
mtClr0 = (GLfloat * 4)(*mtClr0)

light_position0L = [0, 40, -40, 0] # Позиция источника света
lghtClr0L = [0.75, 0, 0, 0] # Цвет источника света

light_position0 = (GLfloat * 4)(*light_position0L)
lghtClr0 = (GLfloat * 4)(*lghtClr0L)

light_position1L = [40, 0, 40, 0] # Позиция источника света
lghtClr1L = [0, 0, 0.75, 0] # Цвет источника света

light_position1 = (GLfloat * 4)(*light_position1L)
lghtClr1 = (GLfloat * 4)(*lghtClr1L)


tz = 0.5
n = 8
h = 40
show_lids = True
show_normals = False
depth_test = True
smooth = True
inner_normalize = True
outer_normalize = True
light = True
culling = True
use_vnorms = True
light1 = True
diffuse = True

# расчет вершин многоугольника
def ngon(r, n, zv, di):
    l = []
    if di == 1:
        start, stop, step = 0, n, 1
    else:
        start, stop, step = n, 0, -1
    for i in range(start, stop, step):
        x = r * np.cos(2 * np.pi * i / n)
        y = r * np.sin(2 * np.pi * i / n)
        l.append([x, y, zv])
    return l

# вычисление нормали к плоскости, построенной на векторах evec1, evec2
def compute_normal(com, a, b, onorm):
    com1, a, b = map(np.array, (com, a, b))
    evec1, evec2 = a - com1, b - com1
    vnorm = np.cross(evec1, evec2)
    if onorm: vnorm = vnorm / np.linalg.norm(vnorm)
    vnorm_end = com1 + vnorm
    vnorm_line = list(vnorm_end) + com
    return vnorm, vnorm_line


# возвращает список нормалей к вершинам b
def vertex_normals(b, t, onorm):
    n = len(b)
    na = np.zeros((n, 3))
    nl = []
    for i in range(n):
        n1,_ = compute_normal(b[i], b[(i+1)%n], t[(n-i)%n], onorm)
        n2,_ = compute_normal(b[i], b[(i+n-1)%n], b[(i+1)%n], onorm)
        n3,_ = compute_normal(b[i], t[(n-i)%n], b[(i+n-1)%n], onorm)
        nnorm = n1 + n2 + n3
        if onorm: nnorm = nnorm / np.linalg.norm(nnorm)
        na[i] = nnorm
        l = list(nnorm + np.array(b[i])) + b[i]
        nl.append(l)
    nl = np.array(nl).flatten()
    return na, nl

lid_top = ngon(35, n, h/2, -1)
lid_bottom = ngon(35, n, -h/2, 1)
norms_bottom, nblines = vertex_normals(lid_bottom, lid_top, outer_normalize)
norms_top, ntlines = vertex_normals(lid_top, lid_bottom, outer_normalize)

def recompute_ngon(n):
    global lid_top, lid_bottom, norms_top, norms_bottom, nblines, ntlines
    lid_top = ngon(35, n, h/2, -1)
    lid_bottom = ngon(35, n, -h/2, 1)
    norms_bottom, nblines = vertex_normals(lid_bottom, lid_top, outer_normalize)
    norms_top, ntlines = vertex_normals(lid_top, lid_bottom, outer_normalize)


# отрисовка осей координат
def draw_coord_lines():
    glDisable(GL_LIGHTING)
    pyglet.graphics.draw(2, GL_LINES, ('v3f', (0, 0, 0, 100, 0, 0)), ('c3f', [1, 0.5, 0] * 2))
    pyglet.graphics.draw(2, GL_LINES, ('v3f', (0, 0, 0, 0, 100, 0)), ('c3f', [0, 1, 0.5] * 2))
    pyglet.graphics.draw(2, GL_LINES, ('v3f', (0, 0, 0, 0, 0, 100)), ('c3f', [0.5, 0, 1] * 2))
    if light: glEnable(GL_LIGHTING)

# отрисовка источников света в виде точек
def draw_light_sources():
    glPushMatrix()
    glLoadIdentity()
    glPointSize(20)
    glDisable(GL_LIGHTING)
    glBegin(GL_POINTS)
    glColor3f(*lghtClr0L[:3])
    glVertex3f(*light_position0L[:3])
    glEnd()
    if light1:
        glBegin(GL_POINTS)
        glColor3f(*lghtClr1L[:3])
        glVertex3f(*light_position1L[:3])
        glEnd()
    if light: glEnable(GL_LIGHTING)
    glPopMatrix()

# отрисовка оснований
def draw_lids():
    glBegin(GL_POLYGON)
    for i, v in enumerate(lid_top):
        glColor3f(0, 0, 1)
        if use_vnorms: glNormal3f(*norms_top[i])
        else: glNormal3f(0, 0, 1)
        glVertex3f(*v)
    glEnd()
    glBegin(GL_POLYGON)
    for i, v in enumerate(lid_bottom):
        glColor3f(0, 0, 1)
        if use_vnorms: glNormal3f(*norms_bottom[i])
        else: glNormal3f(0, 0, -1)
        glVertex3f(*v)
    glEnd()


# отрисовка боковых сторон
def faces(n, norm):
    glLineWidth(3)
    if norm and use_vnorms:
        pyglet.graphics.draw(n*2, GL_LINES, ('v3f', nblines), ('c3f', [1, 1, 0] * n*2))
        pyglet.graphics.draw(n*2, GL_LINES, ('v3f', ntlines), ('c3f', [1, 1, 0] * n*2))

    for i in range(n):
        svl = (lid_bottom[i] , lid_bottom[(i+1)%n] , lid_top[n-1-i] , lid_top[(n-i)%n])
        snl = (norms_bottom[i] , norms_bottom[(i+1)%n] , norms_top[n-1-i] , norms_top[(n-i)%n])
        sn,_ = compute_normal(svl[0], svl[1], svl[3], outer_normalize)
        glBegin(GL_QUADS)
        for j, v in enumerate(svl):
            glColor3f(1, 0, 0)
            if use_vnorms: glNormal3f(*snl[j])
            else: glNormal3f(*sn)
            glVertex3f(*v)
        glEnd()
        if norm and not use_vnorms:
            for v in svl:
                nv = list(sn + np.array(v)) + v
                pyglet.graphics.draw(2, GL_LINES, ('v3f', nv), ('c3f', [1, 1, 0] * 2))


@window.event
def on_draw():
    window.clear()
    glEnable(GL_DEPTH_TEST) if depth_test else glDisable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH) if smooth else glShadeModel(GL_FLAT)
    glEnable(GL_LIGHTING) if light else glDisable(GL_LIGHTING)
    glDisable(GL_CULL_FACE) if culling else glEnable(GL_CULL_FACE)
    glEnable(GL_NORMALIZE) if inner_normalize else glDisable(GL_NORMALIZE)
    glEnable(GL_LIGHT1) if light1 else glDisable(GL_LIGHT1)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mtClr0) if diffuse else glMaterialfv(GL_FRONT, GL_DIFFUSE, (GLfloat * 4)(0, 0, 0, 1.0))

    draw_light_sources()
    draw_coord_lines()
    recompute_ngon(n)
    if show_lids: draw_lids()
    faces(n, show_normals)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    w = 80
    glOrtho(-w, w, -w, w, -w, w)
    #gluPerspective(90, ar, .1, 1000)
    glMatrixMode(GL_MODELVIEW)


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
    global tz, show_lids, show_normals, depth_test, smooth, light, culling
    global outer_normalize, inner_normalize, use_vnorms, n, light1, diffuse
    if symbol == key._1:
        tz = 1
    if symbol == key._2:
        show_lids = not show_lids
    if symbol == key._3:
        smooth = not smooth
    if symbol == key._4:
        light = not light
    if symbol == key._5:
        show_normals = not show_normals
    if symbol == key._6:
        depth_test = not depth_test
    if symbol == key._7:
        culling = not culling
    if symbol == key._8:
        outer_normalize = not outer_normalize
    if symbol == key._9:
        inner_normalize = not inner_normalize
    if symbol == key._0:
        use_vnorms = not use_vnorms
    if symbol == key.PLUS:
        n += 1
    if symbol == key.MINUS:
        n -= 1
    if symbol == key.Q:
        light1 = not light1
    if symbol == key.W:
        diffuse = not diffuse

@window.event
def on_key_release(symbol, modifiers):
    global tz
    if symbol == key._1:
        tz = 0

def rotate(dt):
    global tz, time, light_position0L
    glRotatef(0.5, tz / 20, 0, 0)
    time += dt
    light_position0L = [40*np.cos(time), 40*np.sin(time), 4, 0] # Позиция источника света
    light_position0 = (GLfloat * 4)(*light_position0L)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position0)


if __name__ == "__main__":
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS) # GL_LESS GL_GREATER

    glEnable(GL_LIGHTING)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mtClr0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lghtClr0)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lghtClr1)
    glEnable(GL_LIGHT1)

    pyglet.clock.schedule_interval(rotate, 1/60)
    pyglet.app.run()
