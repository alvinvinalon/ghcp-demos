import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in a Spinning Hexagon")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

class Hexagon:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.angle = 0
        self.rotation_speed = 0.5  # degrees per frame
        self.points = self._calculate_points()
        
        # Store line segments for collision detection
        self.line_segments = []
        self._update_line_segments()

    def _calculate_points(self):
        points = []
        for i in range(6):
            angle = math.radians(self.angle + i * 60)
            x = self.center[0] + self.size * math.cos(angle)
            y = self.center[1] + self.size * math.sin(angle)
            points.append((x, y))
        return points
    
    def _update_line_segments(self):
        self.line_segments = []
        for i in range(6):
            p1 = np.array(self.points[i])
            p2 = np.array(self.points[(i + 1) % 6])
            self.line_segments.append((p1, p2))

    def rotate(self):
        self.angle += self.rotation_speed
        self.points = self._calculate_points()
        self._update_line_segments()

    def draw(self, screen):
        pygame.draw.polygon(screen, WHITE, self.points, 2)
        
        # Draw center point for reference
        pygame.draw.circle(screen, BLUE, self.center, 3)

class Ball:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([2.0, 0.0])  # Initial velocity
        self.radius = 15
        self.mass = 1.0
        self.elasticity = 0.8  # Bounce coefficient (0-1)
        self.gravity = np.array([0.0, 0.2])  # Gravity effect
        self.friction = 0.99  # Friction coefficient
        self.trail = []  # Store positions for trail effect
        self.trail_length = 20
        
    def update(self):
        # Apply gravity
        self.vel += self.gravity
        
        # Apply friction
        self.vel *= self.friction
        
        # Update position
        self.pos += self.vel
        
        # Record position for trail
        self.trail.append(tuple(self.pos.copy()))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def collide_with_segment(self, p1, p2):
        """Handle collision with a line segment defined by p1 and p2"""
        # Vector from p1 to p2
        wall_vec = p2 - p1
        wall_len = np.linalg.norm(wall_vec)
        
        if wall_len == 0:
            return False
            
        # Unit vector along wall
        wall_unit = wall_vec / wall_len
        
        # Vector from wall start to ball
        wall_to_ball = self.pos - p1
        
        # Projection of wall_to_ball onto wall_unit
        proj_length = np.dot(wall_to_ball, wall_unit)
        
        # Get closest point on wall to ball
        if proj_length < 0:
            closest_point = p1
        elif proj_length > wall_len:
            closest_point = p2
        else:
            closest_point = p1 + wall_unit * proj_length
        
        # Check if ball is colliding with wall
        dist_to_wall = np.linalg.norm(self.pos - closest_point)
        
        if dist_to_wall <= self.radius:
            # Calculate wall normal (perpendicular to wall)
            wall_normal = np.array([-wall_vec[1], wall_vec[0]])
            wall_normal = wall_normal / np.linalg.norm(wall_normal)
            
            # Make sure normal points toward the ball
            if np.dot(wall_normal, self.pos - closest_point) < 0:
                wall_normal = -wall_normal
            
            # Calculate reflection direction and apply bounce with elasticity
            incident_vel = self.vel
            reflection = incident_vel - 2 * np.dot(incident_vel, wall_normal) * wall_normal
            self.vel = reflection * self.elasticity
            
            # Move ball outside the wall to prevent sticking
            overlap = self.radius - dist_to_wall
            self.pos = self.pos + wall_normal * (overlap + 0.1)  # Small extra distance to prevent sticking
            
            return True
        
        return False

    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.trail):
            # Fade the trail from transparent to solid
            alpha = int(255 * i / len(self.trail))
            trail_color = (255, 0, 0, alpha)
            trail_radius = int(self.radius * 0.5 * i / len(self.trail))
            
            # Create a surface for the trail circle with transparency
            trail_surface = pygame.Surface((trail_radius*2, trail_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (trail_radius, trail_radius), max(1, trail_radius))
            screen.blit(trail_surface, (int(pos[0])-trail_radius, int(pos[1])-trail_radius))
        
        # Draw main ball
        pygame.draw.circle(screen, RED, self.pos.astype(int), self.radius)

def main():
    hexagon = Hexagon((WIDTH//2, HEIGHT//2), 200)
    ball = Ball(WIDTH//2, HEIGHT//2 - 50)  # Start the ball slightly above center
    
    # Initialize variables for user controls
    paused = False
    show_trail = True
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_t:
                    show_trail = not show_trail
                elif event.key == pygame.K_r:  # Reset
                    ball = Ball(WIDTH//2, HEIGHT//2 - 50)
                elif event.key == pygame.K_UP:
                    hexagon.rotation_speed += 0.1
                elif event.key == pygame.K_DOWN:
                    hexagon.rotation_speed -= 0.1
        
        if not paused:
            # Clear screen
            screen.fill(BLACK)
            
            # Update physics
            hexagon.rotate()
            ball.update()
            
            # Check for collisions with all hexagon sides
            for p1, p2 in hexagon.line_segments:
                ball.collide_with_segment(p1, p2)
            
            # Draw everything
            hexagon.draw(screen)
            ball.draw(screen)
            
            # Display controls
            font = pygame.font.Font(None, 24)
            instructions = [
                "SPACE: Pause/Resume",
                "R: Reset ball",
                "T: Toggle trail",
                "UP/DOWN: Change rotation speed"
            ]
            
            y_pos = 10
            for instruction in instructions:
                text = font.render(instruction, True, WHITE)
                screen.blit(text, (10, y_pos))
                y_pos += 25
                
            # Display physics data
            speed_text = font.render(f"Ball Speed: {np.linalg.norm(ball.vel):.1f}", True, WHITE)
            rotation_text = font.render(f"Rotation: {hexagon.rotation_speed:.1f} deg/frame", True, WHITE)
            screen.blit(speed_text, (WIDTH - 200, 10))
            screen.blit(rotation_text, (WIDTH - 200, 35))
            
            pygame.display.flip()
        
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()