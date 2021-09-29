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
glClear(GL_COLOR_BUFFER_BIT)
py = 0


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


# определяем начальную точку
for i in range(1000):
	startX, startY = getNewXY(startX, startY)


scale = 160 # масштаб
def texInit():
	'''Обновление массива точек - ищем 10000 новых'''
	global startX, startY, scale
	# заполняем белым все
	iWidth = iHeight = 256
	n = 3 * iWidth * iHeight
	img = np.full((iWidth, iHeight, 3), 255, dtype = 'uint8')
	for i in range(10000):
		# если использовать переменную масштаба
		x = int(startX*scale)
		y = int(startY*scale)
		# print(x, y)
		img[x, y] = [0, 0, 0]
		startX, startY = getNewXY(startX, startY)
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

tScale = 2 # d2 / (d2 - d1)
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