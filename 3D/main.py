import math
import pygame
from obj_loader import load_obj

WIDTH, HEIGHT = 1000, 700
BACKGROUND = (15, 15, 30)
WHITE = (255, 255, 255)

CAMERA_DISTANCE = 5
SCALE_2D = 400


def rotate_x(point, angle):
    x, y, z = point
    c = math.cos(angle)
    s = math.sin(angle)
    return [x, y * c - z * s, y * s + z * c]


def rotate_y(point, angle):
    x, y, z = point
    c = math.cos(angle)
    s = math.sin(angle)
    return [x * c + z * s, y, -x * s + z * c]


def rotate_z(point, angle):
    x, y, z = point
    c = math.cos(angle)
    s = math.sin(angle)
    return [x * c - y * s, x * s + y * c, z]


def transform(point, rot_x, rot_y, rot_z, scale, translation):
    # Escala
    p = [coord * scale for coord in point]

    # Rotações
    p = rotate_x(p, rot_x)
    p = rotate_y(p, rot_y)
    p = rotate_z(p, rot_z)

    # Translação
    p[0] += translation[0]
    p[1] += translation[1]
    p[2] += translation[2]

    return p


def project(point):
    x, y, z = point

    # Afasta o objeto da câmera
    z += CAMERA_DISTANCE

    # Evita divisão por zero
    if z <= 0.1:
        z = 0.1

    # Projeção em perspectiva
    factor = SCALE_2D / z
    screen_x = int(x * factor + WIDTH / 2)
    screen_y = int(-y * factor + HEIGHT / 2)

    return (screen_x, screen_y)


class Model3D:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces

        # Transformações do modelo
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0
        self.scale = 1.5
        self.translation = [0.0, 0.0, 0.0]

    def update(self):
        # Rotação automática
        self.rot_y += 0.01

    def draw(self, screen):
        transformed = []

        # Transformar e projetar todos os vértices
        for vertex in self.vertices:
            p = transform(
                vertex,
                self.rot_x,
                self.rot_y,
                self.rot_z,
                self.scale,
                self.translation,
            )
            transformed.append(project(p))

        # Desenhar faces em wireframe
        for face in self.faces:
            points = [transformed[i] for i in face]

            if len(points) >= 3:
                pygame.draw.polygon(screen, WHITE, points, 1)


def handle_input(model):
    keys = pygame.key.get_pressed()

    # Rotação
    if keys[pygame.K_LEFT]:
        model.rot_y -= 0.05
    if keys[pygame.K_RIGHT]:
        model.rot_y += 0.05
    if keys[pygame.K_UP]:
        model.rot_x -= 0.05
    if keys[pygame.K_DOWN]:
        model.rot_x += 0.05
    if keys[pygame.K_q]:
        model.rot_z -= 0.05
    if keys[pygame.K_e]:
        model.rot_z += 0.05

    # Escala
    if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
        model.scale += 0.02
    if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
        model.scale = max(0.1, model.scale - 0.02)

    # Translação
    if keys[pygame.K_a]:
        model.translation[0] -= 0.05
    if keys[pygame.K_d]:
        model.translation[0] += 0.05
    if keys[pygame.K_w]:
        model.translation[1] += 0.05
    if keys[pygame.K_s]:
        model.translation[1] -= 0.05
    if keys[pygame.K_z]:
        model.translation[2] += 0.05
    if keys[pygame.K_x]:
        model.translation[2] -= 0.05


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visualizador 3D em Python")
    clock = pygame.time.Clock()

    # Carrega o modelo OBJ
    vertices, faces = load_obj("cube.obj")
    model = Model3D(vertices, faces)

    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Entrada do usuário
        handle_input(model)

        # Atualização
        model.update()

        # Renderização
        screen.fill(BACKGROUND)
        model.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()