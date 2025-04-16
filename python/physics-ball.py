import pygame
import sys
import math
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize pygame
pygame.init()

# Set up the display
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Bouncing Balls on Rotating Spheres")

# Set background color (dark blue)
glClearColor(0.05, 0.05, 0.2, 1.0)

# Set up the perspective
gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20)  # Move further back to see more of the scene
glEnable(GL_DEPTH_TEST)

# Setup lighting
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

# Light position and properties
light_position = [10.0, 10.0, 10.0, 1.0]  # Positioned further away
light_ambient = [0.4, 0.4, 0.4, 1.0]  # Brighter ambient light
light_diffuse = [1.0, 1.0, 1.0, 1.0]  # Full brightness diffuse
light_specular = [1.0, 1.0, 1.0, 1.0]

glLightfv(GL_LIGHT0, GL_POSITION, light_position)
glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

# Material properties
material_specular = [1.0, 1.0, 1.0, 1.0]
material_shininess = [50.0]
glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

# Function to draw a sphere
def draw_sphere(radius, slices, stacks, color):
    glColor3f(color[0], color[1], color[2])
    sphere = gluNewQuadric()
    gluQuadricNormals(sphere, GLU_SMOOTH)
    gluSphere(sphere, radius, slices, stacks)
    gluDeleteQuadric(sphere)

# Class for the container sphere
class ContainerSphere:
    def __init__(self, radius, position, rotation_speed, color):
        self.radius = radius
        self.position = position  # [x, y, z]
        self.rotation_speed = rotation_speed  # [x_rot, y_rot, z_rot]
        self.rotation = [0, 0, 0]  # Current rotation angles
        self.color = color
    
    def update(self, dt):
        # Update rotation
        self.rotation[0] = (self.rotation[0] + self.rotation_speed[0] * dt) % 360
        self.rotation[1] = (self.rotation[1] + self.rotation_speed[1] * dt) % 360
        self.rotation[2] = (self.rotation[2] + self.rotation_speed[2] * dt) % 360
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Draw the container sphere with visible lines
        glDisable(GL_LIGHTING)
        glColor3f(self.color[0], self.color[1], self.color[2])  # Solid color (no alpha)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        sphere = gluNewQuadric()
        gluQuadricDrawStyle(sphere, GLU_LINE)
        gluSphere(sphere, self.radius, 24, 24)  # More detail
        gluDeleteQuadric(sphere)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_LIGHTING)
        
        glPopMatrix()

# Class for bouncing balls
class Ball:
    def __init__(self, radius, position, velocity, color, container):
        self.radius = radius
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color
        self.container = container
        self.mass = radius ** 3  # Mass proportional to volume
        
        # Ensure ball starts inside the container
        distance = np.linalg.norm(self.position - np.array(container.position))
        if distance + self.radius > container.radius:
            # Adjust position to be inside container
            direction = (self.position - np.array(container.position)) / distance
            self.position = np.array(container.position) + direction * (container.radius - self.radius - 0.01)
    
    def update(self, dt, balls):
        # Apply gravity (optional)
        # self.velocity[1] -= 9.8 * dt  # Gravity in y-direction
        
        # Apply container rotation effect
        # This is a simplified effect - in reality, would need full physics integration
        container_rot_effect = np.array([
            self.container.rotation_speed[1] * 0.01,
            self.container.rotation_speed[0] * -0.01,
            self.container.rotation_speed[2] * 0.01
        ])
        self.velocity += container_rot_effect * dt
        
        # Update position
        self.position += self.velocity * dt
        
        # Check for collision with container
        pos_relative = self.position - np.array(self.container.position)
        distance = np.linalg.norm(pos_relative)
        
        if distance + self.radius > self.container.radius:
            # Ball hit the container wall
            normal = pos_relative / distance
            
            # Position correction (move ball inside)
            penetration = distance + self.radius - self.container.radius
            self.position -= normal * penetration * 1.01  # Move a bit more to avoid floating-point issues
            
            # Velocity reflection with damping
            reflection = self.velocity - 2 * np.dot(self.velocity, normal) * normal
            damping = 0.8  # Energy loss
            self.velocity = reflection * damping
        
        # Check for collisions with other balls
        for other in balls:
            if other is self:
                continue
                
            rel_pos = self.position - other.position
            distance = np.linalg.norm(rel_pos)
            
            if distance < self.radius + other.radius:
                # Collision response
                normal = rel_pos / distance if distance > 0 else np.array([1, 0, 0])
                
                # Position correction
                overlap = self.radius + other.radius - distance
                self.position += normal * overlap * 0.5
                other.position -= normal * overlap * 0.5
                
                # Velocity calculation using conservation of momentum and energy
                v1 = self.velocity
                v2 = other.velocity
                m1 = self.mass
                m2 = other.mass
                
                # Relative velocity along collision normal
                v1_normal = np.dot(v1, normal)
                v2_normal = np.dot(v2, normal)
                
                # Calculate new velocities using elastic collision formula
                restitution = 0.9  # Coefficient of restitution (bounciness)
                
                # New velocities after collision
                new_v1_normal = ((m1 - m2) * v1_normal + 2 * m2 * v2_normal) / (m1 + m2)
                new_v2_normal = ((m2 - m1) * v2_normal + 2 * m1 * v1_normal) / (m1 + m2)
                
                # Apply restitution
                new_v1_normal *= restitution
                new_v2_normal *= restitution
                
                # Update velocities
                self.velocity += normal * (new_v1_normal - v1_normal)
                other.velocity += normal * (new_v2_normal - v2_normal)
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        # Add emission component to make the balls brighter
        emission = [self.color[0] * 0.3, self.color[1] * 0.3, self.color[2] * 0.3, 1.0]
        glMaterialfv(GL_FRONT, GL_EMISSION, emission)
        draw_sphere(self.radius, 16, 16, self.color)
        # Reset emission 
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glPopMatrix()

# Create container spheres - position them to be more visible
containers = [
    ContainerSphere(5.0, [0, 0, 0], [0.1, 0.2, 0.05], [0.5, 0.5, 1.0]),  # Brighter blue
    ContainerSphere(3.0, [8, 0, 0], [0.15, -0.1, 0.1], [0.5, 1.0, 0.5])  # Brighter green, moved to the side
]

# Create balls with random properties
balls = []
colors = [
    [1.0, 0.0, 0.0],  # Red
    [0.0, 1.0, 0.0],  # Green
    [0.0, 0.0, 1.0],  # Blue
    [1.0, 1.0, 0.0],  # Yellow
    [1.0, 0.0, 1.0],  # Magenta
    [0.0, 1.0, 1.0],  # Cyan
    [1.0, 0.5, 0.0],  # Orange
    [0.5, 0.0, 1.0]   # Purple
]

# Add balls to each container
for container in containers:
    num_balls = random.randint(5, 8)  # Fewer balls to avoid potential performance issues
    for i in range(num_balls):
        # Random position inside container (not too close to the edge)
        max_radius = container.radius - 0.5
        theta = random.uniform(0, 2*math.pi)
        phi = random.uniform(0, math.pi)
        r = random.uniform(0, max_radius * 0.7)
        
        position = [
            container.position[0] + r * math.sin(phi) * math.cos(theta),
            container.position[1] + r * math.sin(phi) * math.sin(theta),
            container.position[2] + r * math.cos(phi)
        ]
        
        # Random velocity (reduced for stability)
        velocity = [
            random.uniform(-1.0, 1.0),
            random.uniform(-1.0, 1.0),
            random.uniform(-1.0, 1.0)
        ]
        
        # Random size and color
        radius = random.uniform(0.2, 0.4)
        color = random.choice(colors)
        
        # Create the ball
        ball = Ball(radius, position, velocity, color, container)
        balls.append(ball)

# Camera rotation settings
camera_rotation = [20, 30]  # Start with a different view angle
rotation_speed = 0.5

# Main game loop
clock = pygame.time.Clock()
running = True

# Print controls to the console
print("Controls:")
print("  Arrow keys: Rotate camera")
print("  ESC: Exit simulation")

try:
    while running:
        dt = min(clock.tick(60) / 1000.0, 0.1)  # Delta time in seconds, limit to avoid physics issues
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Rotate camera with keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_rotation[1] -= rotation_speed
        if keys[pygame.K_RIGHT]:
            camera_rotation[1] += rotation_speed
        if keys[pygame.K_UP]:
            camera_rotation[0] += rotation_speed
        if keys[pygame.K_DOWN]:
            camera_rotation[0] -= rotation_speed
        
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set camera rotation
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -20)  # Keep consistent with initial position
        glRotatef(camera_rotation[0], 1, 0, 0)
        glRotatef(camera_rotation[1], 0, 1, 0)
        
        # Update and draw container spheres
        for container in containers:
            container.update(dt)
            container.draw()
        
        # Update and draw balls
        for ball in balls:
            ball.update(dt, balls)
            ball.draw()
        
        # Update the display
        pygame.display.flip()
        
except Exception as e:
    # Print any errors for debugging
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Clean up
    pygame.quit()
    sys.exit()