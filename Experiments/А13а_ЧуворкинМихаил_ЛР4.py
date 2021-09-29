# 50 variant Chain

import numpy as np
from pyglet.gl import *
from pyglet.window import Window
from pyglet import app, graphics
import random


d, d1, d2 = 5, 10, 15
wx, wy = 1.5 * d2, 1.5 * d2
width, height = int(30 * wx), int(30 * wy)
window = Window(visible = True, width = width, height = height, resizable = True)
glClearColor(0.4, 0.4, 0.4, 1.0)
glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glPolygonMode(GL_BACK, GL_LINE) 
glShadeModel(GL_FLAT) # без интерполяции цветов
py = 0

texFromFile = True



def texInit():
	if texFromFile:
		fn = 'D:\\DevPython\\AVTI\\CG_course\\Experiments\\floppa.jpg'
		img = pyglet.image.load(fn)
		iWidth = img.width
		iHeight = img.height
		img = img.get_data('RGB', iWidth * 3)
	else:
		iWidth = iHeight = 64
		n = 3 * iWidth * iHeight
		img = np.zeros((iWidth, iHeight, 3), dtype = 'uint8')
		for i in range(iHeight):
			for j in range(iWidth):
				bw = (i & 16 ^ j & 16)
				img[i, j, :] = bw * 255
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

v0, v1, v2, v3 = (-d2,d2,-zv), (-d2,-d2,-zv), (0,-d2-5,0), (0,d2-5,0)

v4, v5, v6, v7 = (0,d2-5,0), (0,-d2-5, 0), (d2,-d2,-zv), (d2,d2,-zv)

tScale = 1
xoff = tScale / 2
toff = 0.1

def update(dt):
	global py
	if py >= 360:
		py = 0
	else:
		py += 1
	
def updTex(dt):
	global tScale, toff
	if tScale > 5 or tScale < 1:
		toff *= -1
		tScale += toff * 10
	else:
		tScale += toff
		xoff = tScale / 2



pyglet.clock.schedule_interval(update, 1/60)
pyglet.clock.schedule_interval(updTex, 1/20)



@window.event
def on_draw():
	window.clear()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-wx, wx, -wy, wy, -20, 20)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glRotatef(py, 0, 1, 0)
	graphics.draw(8, GL_QUADS,
				  ('v3f', (v0 + v1 + v2 + v3 + v4 + v5 + v6 + v7)),
				  ('t2f', (-tScale,tScale,  -tScale,0,  0,0,  0,tScale,    0,tScale,  0,0,  tScale,0,  tScale,tScale,)))

	# почему-то не работают цвета
	graphics.draw(8, GL_QUADS,
				  ('v3f', (v1 + v0 + v3 + v2 + v5 + v4 + v7 + v6)),
				  ('c3i', (0, 255, 0)*8))

app.run()