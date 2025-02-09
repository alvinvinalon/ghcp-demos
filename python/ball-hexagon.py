import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball in Spinning Hexagon")
clock = pygame.time.Clock()

class Hexagon:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.angle = 0
        self.rotation_speed = 0.5
        self.points = self._calculate_points()

    def _calculate_points(self):
        points = []
        for i in range(6):
            angle = math.radians(self.angle + i * 60)
            x = self.center[0] + self.size * math.cos(angle)
            y = self.center[1] + self.size * math.sin(angle)
            points.append((x, y))
        return points

    def rotate(self):
        self.angle += self.rotation_speed
        self.points = self._calculate_points()

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.points, 2)

class Ball:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0])
        self.radius = 10
        self.gravity = np.array([0.0, 0.3])
        self.bounce_damping = 0.8
        self.friction = 0.99
        self.max_jump_force = 15.0  # Maximum jump velocity

    def jump(self, charge_time):
        # Calculate jump force based on charge time (max 1 second)
        force = min(charge_time / 1000.0, 1.0) * self.max_jump_force
        self.vel[1] = -force  # Negative because y-axis points downward

    def update(self):
        self.vel = self.vel * self.friction
        self.vel += self.gravity
        self.pos += self.vel

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.pos.astype(int), self.radius)

def line_intersection(p1, p2, circle_pos, radius):
    # Vector from p1 to p2
    line_vec = p2 - p1
    # Vector from p1 to circle center
    circle_vec = circle_pos - p1
    line_length = np.linalg.norm(line_vec)
    line_unit_vec = line_vec / line_length
    proj_length = np.dot(circle_vec, line_unit_vec)
    
    if proj_length < 0 or proj_length > line_length:
        return False

    proj_point = p1 + line_unit_vec * proj_length
    distance = np.linalg.norm(circle_pos - proj_point)
    return distance <= radius

def main():
    hexagon = Hexagon((WIDTH//2, HEIGHT//2), 200)
    ball = Ball(WIDTH//2, HEIGHT//2)
    
    space_pressed = False
    space_press_time = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                    space_press_time = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and space_pressed:
                    charge_time = pygame.time.get_ticks() - space_press_time
                    ball.jump(charge_time)
                    space_pressed = False

        screen.fill((0, 0, 0))
        hexagon.rotate()
        ball.update()

        # Show charging indicator when space is pressed
        if space_pressed:
            charge_time = pygame.time.get_ticks() - space_press_time
            charge_percent = min(charge_time / 1000.0, 1.0)
            indicator_height = 50 * charge_percent
            pygame.draw.rect(screen, (0, 255, 0), (10, HEIGHT - 60, 20, indicator_height))

        # Check collisions with all hexagon sides
        for i in range(6):
            p1 = np.array(hexagon.points[i])
            p2 = np.array(hexagon.points[(i + 1) % 6])
            
            if line_intersection(p1, p2, ball.pos, ball.radius):
                # Calculate normal vector of the wall
                wall_vec = p2 - p1
                wall_normal = np.array([-wall_vec[1], wall_vec[0]])
                wall_normal = wall_normal / np.linalg.norm(wall_normal)
                
                # Reflect velocity vector
                ball.vel = ball.vel - 2 * np.dot(ball.vel, wall_normal) * wall_normal
                ball.vel *= ball.bounce_damping
                
                # Move ball away from wall to prevent sticking
                overlap = ball.radius - np.abs(np.dot(ball.pos - p1, wall_normal))
                if overlap > 0:
                    ball.pos += wall_normal * overlap

        hexagon.draw(screen)
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
