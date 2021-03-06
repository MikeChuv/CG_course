
from pyglet.gl import *
import pyglet
from pyglet import app, graphics
from pyglet.window import Window, key
import numpy as np

d, d1, d2 = 5, 10, 15
wx, wy = 1.5 * d2, 1.5 * d2
width, height = int(30 * wx), int(30 * wy)
window = Window(visible = True, width = width, height = height, resizable = True)
glClearColor(0.4, 0.4, 0.4, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
py = 0

def texInit():
	iWidth = iHeight = 64
	n = 3 * iWidth * iHeight
	img = np.zeros((iWidth, iHeight, 3), dtype = 'uint8')
	for i in range(iHeight):
		for j in range(iWidth):
			bw = (i & 32) ^ (j & 32)
			img[i, j, :] = bw * 255, 255,255
	img = img.reshape(n)
	img = (GLubyte * n)(*img)
	p, r = GL_TEXTURE_2D, GL_RGB
	glTexParameterf(p, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(p, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(p, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(p, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	glTexImage2D(p, 0, r, iWidth, iHeight, 0, r, GL_UNSIGNED_BYTE, img)
	glEnable(p)

texInit()
zv = -d2/2
v0, v1, v2, v3 = (-d2,d2, 0), (-d1,d1,zv), (d1,d1,zv), (d2,d2,0)


def update(dt):
	global py
	if py >= 360:
		py = 0
	else:
		py += 1


#pyglet.clock.schedule_interval(update, 1/60)

tScale = 3 # d2 / (d2 - d1)
xoff = tScale / 6

@window.event
def on_draw():
	window.clear()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-wx, wx, -wy, wy, -20, 20)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glRotatef(py, 1, 0, 0)
	graphics.draw(4, GL_POLYGON,
				  ('v3f', (v0 + v1 + v2 + v3)),
				  ('t2f', (0,tScale, xoff,0, tScale - xoff,0, tScale,tScale)))

app.run()
