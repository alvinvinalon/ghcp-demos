import os
import time
import random

# On Windows, use msvcrt for non-blocking key input
try:
    import msvcrt  # type: ignore
    HAS_MSVCRT = True
except Exception:  # Fallback (blocking input)
    HAS_MSVCRT = False

# Game settings
GRID_WIDTH = 20
GRID_HEIGHT = 15
SNAKE_START_LENGTH = 3
SLEEP_TIME = 0.12  # frame delay (seconds)

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}


def clear_screen() -> None:
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def place_food(snake: list[tuple[int, int]]) -> tuple[int, int]:
    """Place food at a random empty position."""
    empty = [(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH) if (x, y) not in snake]
    return random.choice(empty) if empty else (-1, -1)


def draw_grid(snake: list[tuple[int, int]], food: tuple[int, int], score: int) -> None:
    """Render the game state to the console."""
    snake_set = set(snake)
    # Top border
    print("#" * (GRID_WIDTH + 2))
    for y in range(GRID_HEIGHT):
        row = ["#"]
        for x in range(GRID_WIDTH):
            if (x, y) == snake[0]:
                row.append("O")  # head
            elif (x, y) in snake_set:
                row.append("o")  # body
            elif (x, y) == food:
                row.append("*")  # food
            else:
                row.append(" ")
        row.append("#")
        print("".join(row))
    # Bottom border
    print("#" * (GRID_WIDTH + 2))
    print(f"Score: {score}    Controls: WASD or Arrow Keys | Q to quit")


def read_direction(current: str) -> str:
    """Read a direction from keyboard if available (Windows), else keep current.

    Prevent reversing into itself.
    """
    opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    wanted = None

    if HAS_MSVCRT and msvcrt.kbhit():
        key = msvcrt.getch()
        # Arrow keys come as a prefix (b'\xe0' or b'\x00') then a code
        if key in (b"\xe0", b"\x00"):
            code = msvcrt.getch()
            mapping = {b"H": "UP", b"P": "DOWN", b"K": "LEFT", b"M": "RIGHT"}
            wanted = mapping.get(code)
        else:
            k = key.decode(errors="ignore").lower()
            if k == "w":
                wanted = "UP"
            elif k == "s":
                wanted = "DOWN"
            elif k == "a":
                wanted = "LEFT"
            elif k == "d":
                wanted = "RIGHT"
            elif k == "q":
                # Immediate quit
                raise KeyboardInterrupt

    if wanted and wanted != opposite[current]:
        return wanted
    return current


def step(snake: list[tuple[int, int]], direction: str, food: tuple[int, int]):
    """Advance the game by one step.

    Returns: (alive: bool, new_snake, new_food, ate: bool)
    """
    dx, dy = DIRECTIONS[direction]
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Check wall collision
    if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
        return False, snake, food, False
    # Check self collision (allow moving into current tail position before it moves)
    if new_head in snake[:-1]:
        return False, snake, food, False

    new_snake = [new_head] + snake[:]  # grow by default; pop if not eating
    ate = new_head == food
    if not ate:
        new_snake.pop()  # move without growth
        new_food = food
    else:
        new_food = place_food(new_snake)

    return True, new_snake, new_food, ate


def init_snake() -> list[tuple[int, int]]:
    """Create starting snake centered, heading RIGHT."""
    cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
    return [(cx - i, cy) for i in range(SNAKE_START_LENGTH)]


def play_game() -> None:
    snake = init_snake()
    direction = "RIGHT"
    food = place_food(snake)
    score = 0

    while True:
        clear_screen()
        draw_grid(snake, food, score)

        try:
            direction = read_direction(direction)
        except KeyboardInterrupt:
            print("\nQuitting...")
            break

        alive, snake, food, ate = step(snake, direction, food)
        if not alive:
            clear_screen()
            draw_grid(snake, food, score)
            print("Game Over!")
            break
        if ate:
            score += 1

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nExiting...")
