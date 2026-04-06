import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ---------- Cubo ----------
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0,1),(0,3),(0,4),
    (2,1),(2,3),(2,7),
    (6,3),(6,4),(6,7),
    (5,1),(5,4),(5,7)
)

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# ---------- Eixos ----------
def draw_axes():
    glBegin(GL_LINES)

    # X - vermelho
    glColor3f(1, 0, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f(10, 0, 0)

    # Y - verde
    glColor3f(0, 1, 0)
    glVertex3f(0, -10, 0)
    glVertex3f(0, 10, 0)

    # Z - azul
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -10)
    glVertex3f(0, 0, 10)

    glEnd()

# ---------- Inicialização ----------
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -25)

clock = pygame.time.Clock()

angle = 0

# ---------- Loop principal ----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_axes()

    angle += 1  # velocidade angular (igual para todos)

    # ---------- +X ----------
    glPushMatrix()
    glTranslatef(6, 0, 0)
    glRotatef(angle, 1, 0, 0)  # eixo X
    glColor3f(1, 1, 1)
    draw_cube()
    glPopMatrix()

    # ---------- -X ----------
    glPushMatrix()
    glTranslatef(-6, 0, 0)
    glRotatef(angle, 1, 0, 0)
    draw_cube()
    glPopMatrix()

    # ---------- +Y ----------
    glPushMatrix()
    glTranslatef(0, 6, 0)
    glRotatef(angle, 0, 1, 0)  # eixo Y
    draw_cube()
    glPopMatrix()

    # ---------- -Y ----------
    glPushMatrix()
    glTranslatef(0, -6, 0)
    glRotatef(angle, 0, 1, 0)
    draw_cube()
    glPopMatrix()

    # ---------- +Z ----------
    glPushMatrix()
    glTranslatef(0, 0, 6)
    glRotatef(angle, 0, 0, 1)  # eixo Z
    draw_cube()
    glPopMatrix()

    # ---------- -Z ----------
    glPushMatrix()
    glTranslatef(0, 0, -6)
    glRotatef(angle, 0, 0, 1)
    draw_cube()
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()