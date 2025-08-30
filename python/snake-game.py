import time
import random
import os  # For clearing the screen

# Game settings
GRID_WIDTH = 20
GRID_HEIGHT = 15
SNAKE_START_LENGTH = 3
FOOD_PROBABILITY = 0.1  # Chance of food appearing each step
SLEEP_TIME = 0.1  # Adjust for game speed

# Snake representation (list of coordinates: [(x1, y1), (x2, y2), ...])
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Starting position
direction = "RIGHT"  # Initial direction
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
food_appeared = True

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def draw_grid():
    """Prints the game grid."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in snake:
                print("O", end="")  # Snake body
            elif (x, y) == food:
                print("F", end="")  # Food
            else:
                print(".", end="")  # Empty space
        print()

def move_snake():
    """Moves the snake one step in the current direction."""
    global direction
    head_x, head_y = snake[0]

    if direction == "UP":
        new_head = (head_x, head_y - 1)
    elif direction == "DOWN":
        new_head = (head_x, head_y + 1)
    elif direction == "LEFT":
        new_head = (head_x - 1, head_y)
    elif direction == "RIGHT":
        new_head = (head_x + 1, head_y)

    # Check for collisions
    if (
        new_head[0] < 0
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0
        or new_head[1] >= GRID_HEIGHT
        or new_head in snake
    ):
        return False  # Game over

    snake.insert(0, new_head)  # Add new head
    snake.pop()  # Remove tail

    # Generate new food if the snake hasn't eaten
    if not food_appeared:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        food_appeared = True

    return True  # Game continues

def play_game():
    """Runs the main game loop."""
    while True:
        clear_screen()
        draw_grid()

        key = input("Use W/A/S/D to move. Press Q to quit: ").upper()

        if key == 'Q':
            break

        if key == 'W':
            direction = "UP"
        elif key == 'S':
            direction = "DOWN"
        elif key == 'A':
            direction = "LEFT"
        elif key == 'D':
            direction = "RIGHT"

        if move_snake():
            time.sleep(SLEEP_TIME) # Adjust for speed
        else:
            print("Game Over!")
            break


if __name__ == "__main__":
    import time
    play_game()
