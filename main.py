import pygame
import math

pygame.font.init()
FONT = pygame.font.SysFont('Comic Sans MS', 30)

screen_width, screen_height = 1920, 1080
pygame.display.set_caption("Mesh Render")
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

fov = 300

# cube render
verts_cube = [
    [60, 60, 60],
    [60, -60, -60],
    [-60, 60, -60],
    [-60, -60, -60],
    [60, -60, 60],
    [60, 60, -60],
    [-60, 60, 60],
    [-60, -60, 60]
]
verts_rect = [
    [120, 60, 60],
    [120, -60, -60],
    [-120, 60, -60],
    [-120, -60, -60],
    [120, -60, 60],
    [120, 60, -60],
    [-120, 60, 60],
    [-120, -60, 60]
]
verts_pyramid = [
    [60, 60, 60],
    [0, -60, 0],
    [-60, 60, -60],
    [0, -60, 0],
    [0, -60, 0],
    [60, 60, -60],
    [-60, 60, 60],
    [0, -60, 0]
]
edges = [
    [0, 5],
    [1, 5],
    [5, 2],
    [2, 3],
    [4, 1],
    [4, 0],
    [4, 7],
    [7, 3],
    [7, 6],
    [6, 2],
    [0, 6],
    [3, 1]
]

def project(x, y, z, focal_length):
    x_projected = (focal_length * x) // (focal_length + z - 100) + screen_width/2
    y_projected = (focal_length * y) // (focal_length + z - 100) + screen_height/2

    return x_projected, y_projected

def multiply_vector(v1, v2):
    return [sum(v1[i][j] * v2[j] for j in range(3)) for i in range(3)]

def add_vector(v1, v2):
    x = v1[0] + v2[0]
    y = v1[1] + v2[1]
    z = v1[2] + v2[2]
    return [x, y, z]

def rotate_vert(xa, ya, za, x, y, z):
    x_matrix = [
        [1, 0, 0],
        [0, math.cos(xa), -math.sin(xa)],
        [0, math.sin(xa), math.cos(xa)]
    ]
    y_matrix = [
        [math.cos(ya), 0, math.sin(ya)],
        [0, 1, 0],
        [-math.sin(ya), 0, math.cos(ya)]
    ]
    z_matrix = [
        [math.cos(za), -math.sin(za), 0],
        [math.sin(za), math.cos(za), 0],
        [0, 0, 1]
    ]
    
    x_m_sum = multiply_vector(x_matrix, [x, y, z])
    y_m_sum = multiply_vector(y_matrix, x_m_sum)
    z_m_sum = multiply_vector(z_matrix, y_m_sum)
    return  z_m_sum

def main():
    running = True

    x_rotation = 0
    y_rotation = -30
    z_rotation = 0

    cam_x = 0
    cam_y = 0
    cam_z = 0

    clock = pygame.time.Clock()

    rendering = verts_cube

    show_verticies = True

    cube_path = "images/cube.png"
    pyramid_path = "images/pyramid.png"
    rect_path = "images/rectangle.png"

    while running:
        clock.tick(75)

        #x_rotation += 1
        y_rotation += -1
        #z_rotation += 1

        # make buttons
        cube_button = pygame.Rect(10, 10, 80, 80)
        pyramid_button = pygame.Rect(100, 10, 80, 80)
        rectangle_button = pygame.Rect(190, 10, 80, 80)
        show_verticies_button = pygame.Rect(10, screen_height - 90, 240, 80)

        # make text
        text = "Show verticies"
        if show_verticies:
            text = "Hide verticies"
        show_vert_text = FONT.render(text, True, BLACK)

        # make images
        pyramid_img = pygame.transform.scale(pygame.image.load(pyramid_path), (70, 70))
        rect_img = pygame.transform.scale(pygame.image.load(rect_path), (70, 70))
        cube_img = pygame.transform.scale(pygame.image.load(cube_path), (70, 70))

        # quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if cube_button.collidepoint(mouse_x, mouse_y):
                    rendering = verts_cube
                if pyramid_button.collidepoint(mouse_x, mouse_y):
                    rendering = verts_pyramid
                if rectangle_button.collidepoint(mouse_x, mouse_y):
                    rendering = verts_rect
                if show_verticies_button.collidepoint(mouse_x, mouse_y):
                    show_verticies = not show_verticies


        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pass #cam_x += 2
        
        # update
        screen.fill(WHITE)

        # show buttons
        pygame.draw.rect(screen, BLACK, cube_button, 5)
        pygame.draw.rect(screen, BLACK, pyramid_button, 5)
        pygame.draw.rect(screen, BLACK, rectangle_button, 5)
        pygame.draw.rect(screen, BLACK, show_verticies_button, 5)

        # show images/text on buttons
        screen.blit(show_vert_text, (120 - show_vert_text.get_width()/2, screen_height - 75))

        screen.blit(cube_img, (15, 15))
        screen.blit(pyramid_img, (105, 15))
        screen.blit(rect_img, (195, 15))

         # render edges
        for edge in edges:
            vert_a, vert_b = edge
            vert_a_pos = rendering[vert_a]
            vert_b_pos = rendering[vert_b]

            cax, cay, caz = add_vector(vert_a_pos, [cam_x, cam_y, cam_z])
            cbx, cby, cbz = add_vector(vert_b_pos, [cam_x, cam_y, cam_z])

            ax, ay, az = rotate_vert(math.radians(x_rotation), math.radians(y_rotation), math.radians(z_rotation), cax, cay, caz)
            bx, by, bz = rotate_vert(math.radians(x_rotation), math.radians(y_rotation), math.radians(z_rotation), cbx, cby, cbz)
            apx, apy = project(ax, ay, az, fov)
            bpx, bpy = project(bx, by, bz, fov)
            pygame.draw.line(screen, BLACK, (apx, apy), (bpx, bpy), 4)
        
        # render vertices
        if show_verticies:
            for vert in rendering:
                cx, cy, cz = vert
                x, y, z = rotate_vert(math.radians(x_rotation), math.radians(y_rotation), math.radians(z_rotation), cx, cy, cz)
                x_project, y_project = project(x, y, z, fov)
                pygame.draw.circle(screen, RED, (x_project, y_project), 5)

        pygame.display.flip()

if __name__ == "__main__":
    main()