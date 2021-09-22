
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
texFromFile = True

vlist = []
tlist = []
def ngon(xoff, yoff, r, n):
	for i in range(n):
		x = xoff + r * np.cos(2 * np.pi * i / n)
		tx = np.cos(2 * np.pi * i / n)
		y = yoff + r * np.sin(2 * np.pi * i / n)
		ty = np.sin(2 * np.pi * i / n)
		vlist.append((x, y))
		tlist.append((tx, ty))


def texInit():
	if texFromFile:
		fn = 'D:\\DevPython\\AVTI\\CG_course\\03_Textures\\zzebra.jpg'
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
				bw = (i & 32 ^ j & 32)
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

n = 5
ngon(0, 0, 10, n)

def make_tuple(vl):
	v = ()
	for el in vl:
		v += el
	return v

@window.event
def on_draw():
	window.clear()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-wx, wx, -wy, wy, -20, 20)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	graphics.draw(n, GL_POLYGON,
				  ('v2f', make_tuple(vlist)),
				  ('t2f', make_tuple(tlist)))

app.run()
