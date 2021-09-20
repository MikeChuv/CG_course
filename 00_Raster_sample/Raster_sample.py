import numpy as np
from pyglet.gl import *
from pyglet.window import Window
from pyglet import app
# width
w = 200
# fill 3dim np array with white color (all channels are equal to 255) 
vp = np.full((w, w, 3), 255, dtype = 'uint8')
lineW = 3
for i in range(w):
    # (y = x line)
    i0, i2 = i - lineW, i + lineW # i0 master diag offsets (4 pixels in x,y)
    vp[i0 : i2, i0 : i2] = [0, 255, 0] # green master diag
    # (y = -x line)
    i00, i20 = w - i0 - 1, w - i2 - 1
    vp[i0:i2, i20:i00] = [0, 255, 0] # green slave diag
vp[-lineW:, :] = vp[:lineW, :] = [255, 0, 255] # blue horisontal lines 
vp[:, -lineW:] = vp[:, :lineW] = [0, 0, 255] # blue vertical lines
k = w // 4 # calc square start point
k2 = 3 * k # calc square end point
vp[k:k2, k:k2] = [255, 0, 0] # red square
# flatten makes 1d array from 2d array
vp = vp.flatten()
# cast to GL unsigned byte
vp = (GLubyte * (w * w * 3))(*vp)
window = Window(visible = True, width = w, height = w, caption = 'vp', resizable = 1)
@window.event
def on_draw():
    window.clear()
    # draw w * w pixels in RGB colorspace (vp data)
    glDrawPixels(w, w, GL_RGB, GL_UNSIGNED_BYTE, vp)
app.run()