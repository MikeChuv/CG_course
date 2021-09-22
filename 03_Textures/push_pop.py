#
# Угол поворот в glRotatef меняется после нажатия на 1 (key._1) 
#
from pyglet.gl import *
from pyglet import app, graphics
from pyglet.window import Window, key
# Окно вывода
w = 400
h = 400
window = Window(visible = True, width = w, height = h,
                resizable = True, caption = 'PUSH_POP')
glClearColor(0.1, 0.1, 0.1, 1.0)
glClear(GL_COLOR_BUFFER_BIT)
glPolygonMode(GL_FRONT, GL_FILL) # Заливка лицевой стороны
 
push_pop = True
px = py = 0
@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-4, 4, -4, 4, -1, 1) # Прямоугольное проецирование
    glLineWidth(6)
    # Аффинные преобразования выполняем в мировой система координат
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(180*px, 1, 0, 0) # Поворот вокруг оси X
    glRotatef(180*py, 0, 1, 0) # Поворот вокруг оси Y
    if push_pop:
        glPushMatrix()      #  Заносим матрицу поворота в стек
        glLoadIdentity()    #  Делаем матрицу GL_VODELVIEW делаем единичной
    graphics.draw(4, GL_LINES,      # Рисуем оси координат без какого-либо воздействия на них glRotatef()
                 ('v2f', (-4, 0, 4, 0, 0, -4, 0, 4)),
                 ('c3f', (1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0)))
 
    glLineWidth(4)
    glColor3f(0, 1, 0)
    if push_pop: glPopMatrix()  # Извлекаем из стека матрицу поворота
    graphics.draw(4, GL_QUADS, ('v2f', (-3,-3, -1,-3, -1,-1, -3,-1)))   # рисуем квадрат, который можно вращать
@window.event
def on_key_press(symbol, modifiers):
    global px, py, push_pop
    if symbol == key._1:
        px = 1 - px
        py = 1 - py
    if symbol == key._2:
        push_pop = not push_pop
app.run()