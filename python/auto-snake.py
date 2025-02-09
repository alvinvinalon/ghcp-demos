import pygame, sys, random

pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
FPS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# Directions
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Snake Duel")
clock = pygame.time.Clock()

# Snake structure
def create_snake(start_pos, init_direction):
    return {"body": [start_pos],
            "direction": init_direction,
            "score": 0}

snake1 = create_snake((CELL_SIZE * 5, CELL_SIZE * 5), DIRECTIONS["RIGHT"])
snake2 = create_snake((WIDTH - CELL_SIZE * 5, HEIGHT - CELL_SIZE * 5), DIRECTIONS["LEFT"])

def get_random_food():
    cols = WIDTH // CELL_SIZE
    rows = HEIGHT // CELL_SIZE
    return (random.randint(0, cols - 1) * CELL_SIZE, random.randint(0, rows - 1) * CELL_SIZE)

food = get_random_food()

def will_collide(pos, snake):
    return pos in snake["body"]

def valid_position(pos, snake_a, snake_b):
    x, y = pos
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return False
    if pos in snake_a["body"] or pos in snake_b["body"]:
        return False
    return True

def choose_direction(snake, other_snake, food):
    head = snake["body"][0]
    possible = []
    # Prioritize horizontal or vertical movement toward food
    if food[0] < head[0]:
        possible.append(DIRECTIONS["LEFT"])
    elif food[0] > head[0]:
        possible.append(DIRECTIONS["RIGHT"])
    if food[1] < head[1]:
        possible.append(DIRECTIONS["UP"])
    elif food[1] > head[1]:
        possible.append(DIRECTIONS["DOWN"])
    
    # Add all directions as fallback
    for d in [DIRECTIONS["UP"], DIRECTIONS["DOWN"], DIRECTIONS["LEFT"], DIRECTIONS["RIGHT"]]:
        if d not in possible:
            possible.append(d)

    # Choose first valid direction (avoid immediate collision & opponent's head)
    for d in possible:
        new_head = (head[0] + d[0]*CELL_SIZE, head[1] + d[1]*CELL_SIZE)
        # Avoid moving into the opponent's head
        if new_head == other_snake["body"][0]:
            continue
        if valid_position(new_head, snake, other_snake):
            return d
    return snake["direction"]

game_over = False
winner_text = ""

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Autonomous decision for each snake
        snake1["direction"] = choose_direction(snake1, snake2, food)
        snake2["direction"] = choose_direction(snake2, snake1, food)
        
        # Calculate new heads
        new_head1 = (snake1["body"][0][0] + snake1["direction"][0]*CELL_SIZE,
                     snake1["body"][0][1] + snake1["direction"][1]*CELL_SIZE)
        new_head2 = (snake2["body"][0][0] + snake2["direction"][0]*CELL_SIZE,
                     snake2["body"][0][1] + snake2["direction"][1]*CELL_SIZE)

        # Check head-to-head collision
        if new_head1 == new_head2:
            game_over = True
            winner_text = "Both snakes collided head-on!"
        # Check collisions (walls or body collisions)
        elif not valid_position(new_head1, snake1, snake2):
            game_over = True
            winner_text = "Snake2 wins (Snake1 crashed)!"
        elif not valid_position(new_head2, snake2, snake1):
            game_over = True
            winner_text = "Snake1 wins (Snake2 crashed)!"
        else:
            # Move snakes
            snake1["body"].insert(0, new_head1)
            snake2["body"].insert(0, new_head2)

            # Check if food eaten by snake1
            if new_head1 == food:
                snake1["score"] += 1
                food = get_random_food()
            else:
                snake1["body"].pop()

            # Check if food eaten by snake2
            if new_head2 == food:
                snake2["score"] += 1
                food = get_random_food()
            else:
                snake2["body"].pop()

            # Check winning score (10)
            if snake1["score"] >= 10:
                game_over = True
                winner_text = "Snake1 wins by score!"
            elif snake2["score"] >= 10:
                game_over = True
                winner_text = "Snake2 wins by score!"

    # Draw everything
    screen.fill(BLACK)
    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    # Draw snakes
    for segment in snake1["body"]:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    for segment in snake2["body"]:
        pygame.draw.rect(screen, BLUE, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    # Draw scores
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f"Snake1: {snake1['score']}  Snake2: {snake2['score']}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw winner message if game over
    if game_over:
        win_text = font.render(winner_text, True, WHITE)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
    
    pygame.display.flip()
    clock.tick(FPS)
