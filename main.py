# main.py

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# --- Constants and Setup ---
# This part of the code sets up our game window, colors, and the size of our world.
# You don't need to change this, but it's good to see how it's done!

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 580
UI_HEIGHT = 100
GAME_HEIGHT = WINDOW_HEIGHT - UI_HEIGHT
TILE_SIZE = 40

# Perception
# STEP 0: Set the rover's starting position and direction.
# Rover variables
rover_x = 1
rover_y = 1
rover_direction = 0  # 0=North, 1=East, 2=South, 3=West

# STEP 1: Calculate the width and height of the map in tiles.
# The game area is GAME_HEIGHT pixels tall and WINDOW_WIDTH pixels wide.
# How many tiles can fit in that space?
# Hint: Use integer division //
MAP_WIDTH = WINDOW_WIDTH // TILE_SIZE
MAP_HEIGHT = GAME_HEIGHT // TILE_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create screen and clock
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mars Rover Rescue!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# --- Load Game Assets ---
# Here we load the images we need for our game.

# The rover sprite is already loaded for you.
player_sprite = pygame.image.load("assets/rover.png")
player_sprite = pygame.transform.scale(player_sprite, (TILE_SIZE, TILE_SIZE))

# STEP 2: Load the rock and goal sprites. You can find the assets in the assets folder.
# They should also be scaled to fit our TILE_SIZE.
# Use pygame.image.load() and pygame.transform.scale() like the rover example.
obstacle_sprite = pygame.image.load("assets/rock.png")
obstacle_sprite = pygame.transform.scale(obstacle_sprite, (TILE_SIZE, TILE_SIZE))

goal_sprite = pygame.image.load("assets/flag.png")
goal_sprite = pygame.transform.scale(goal_sprite, (TILE_SIZE, TILE_SIZE))

# STEP 3: Load the mars background image.
# Should the background fit the tile size or the whole game area?
mars_background = pygame.image.load("assets/mars.png")
mars_background = pygame.transform.scale(mars_background, (WINDOW_WIDTH, GAME_HEIGHT))

# --- Map and Rover Data ---
# These variables and functions control the map layout and the rover's state.

# The 'map' is a 2D list (a list of lists). 0 means empty floor, 1 means wall.

map = []


def create_default_map():
    """Create a default map with walls. You don't need to edit this."""
    global map
    map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
           [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
           [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
           [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
           [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


def create_empty_map():
    """Create an empty map for drawing."""
    global map

    # STEP 4: Create an empty map.
    # Use for loops to fill the map with the value for empty floor.
    # The map should be MAP_HEIGHT rows tall and MAP_WIDTH columns wide.
    for list in range(MAP_HEIGHT):
        for grid in range(MAP_WIDTH):
            map[list][grid] = 0

    # STEP 5: Fill the map with boundary walls.
    # Use for loops to set the first and last rows and columns to 1 (walls).
    # Hint: The first row and last rows are done for you.
    for column in range(MAP_WIDTH):
        map[0][column] = 1
        map[MAP_HEIGHT - 1][column] = 1
    # Complete the loop to fill the first and last columns with walls.
    for row in range(MAP_HEIGHT):
        map[row][0] = 1
        map[row][MAP_WIDTH -1] = 1


# We initially create a default map.
create_default_map()

rover_trail = []

# STEP 6: Set the goal position to the bottom-right corner of the map.
goal_x = MAP_WIDTH - 2
goal_y = MAP_HEIGHT - 2

# Game state
drawing_mode = True
algorithm_running = False
game_won = False
algorithm_steps = 0
current_algorithm = "wall_follower"  # "wall_follower" or "random_mouse"

# STEP 7: Create a list of direction vectors and their names.
# Direction vectors: (dx, dy) for North, East, South, West
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
# These directions are jumbled up! Fix them.
direction_names = ["North", "East", "South", "West"]

# --- ROVER'S BRAIN - This is the main code! ---


def can_move(x, y):
    """Check if the rover can move to position (x, y)."""
    # STEP 8: Complete this function.
    # The rover can move to (x, y) if it's inside the map boundaries
    # AND the tile at that position in the 'map' list is a floor (value 0).
    # Hint: The map is accessed with map[y][x].
    # Check if the tile is a floor (0) or a wall (1)
    if map[y][x] == 1:
        return False
    return True


def turn_right():
    """Turn the rover 90 degrees to the right."""
    global rover_direction
    # STEP 9: Change the rover's direction.
    # Directions are 0, 1, 2, 3. What happens when you add 1 to 3? It should come back to 0.
    # Hint: The modulo operator (%) is perfect for this! `3 % 4` is 0.
    # Hint: The modulo operator gives us th remainder of a division.
    rover_direction = (rover_direction + 1) % 4


def turn_left():
    """Turn the rover 90 degrees to the left."""
    global rover_direction
    # STEP 10: Change the rover's direction.
    # This is similar to turning right, but you do the opposite.
    # Hint: `(0 - 1) % 4` in Python is 3. Perfect!
    rover_direction = (rover_direction - 1) % 4


def move_rover(dx, dy):
    """Try to move the rover by (dx, dy)."""
    global rover_x, rover_y
    # STEP 11: Complete this function.
    # 1. Calculate the new potential position (new_x, new_y).
    # 2. Use your `can_move()` function to check if this new spot is valid.
    # 3. If it is valid, update the rover's `rover_x` and `rover_y`.
    # 4. Also, add the *old* position to the `rover_trail` list to show where we've been.
    new_x = rover_x + dx
    new_y = rover_y + dy
    
    #If true it will execute
    if can_move(new_x, new_y):
        # Add the current position to the trail BEFORE you move.
        rover_trail.append((rover_x, rover_y))
        # Update the rover's position to the new position.
        rover_x = new_x
        rover_y = new_y
        return True  # We successfully moved!
    return False  # We hit a wall.


def wall_follower_step():
    """Perform one step of the 'right-hand wall following' algorithm."""
    global algorithm_steps

    # STEP 12: Implement the wall-following logic.
    # This is the rover's escape plan! It always tries to keep a wall on its right.
    #
    # The Plan:
    # 1. First, turn right to "feel" for the wall.
    # 2. Try to move forward in this new direction. If you can, you're done for this step!
    # 3. If you can't (because there's a wall), turn back to where you were facing.
    # 4. Now, try to move forward in the original direction. If you can, great!
    # 5. If you STILL can't move forward, you must be in a corner. Turn left as a last resort.
    #
    # Use the functions you just wrote: turn_right(), turn_left(), move_rover(), and the 'directions' list.

    # --- Your code goes below ---

    # 1. Turn right
    turn_right()

    # Get the change in x and y for the new direction
    dx, dy = directions[rover_direction]

    # 2. Try to move forward (in the new "right" direction)
    if move_rover(dx, dy):
        pass  # We successfully moved, nothing else to do this step!
    else:
        # 3. We couldn't move right, so turn back left (to our original direction)
        turn_left()

        # Get the new dx, dy for this direction
        dx, dy = directions[rover_direction]

        # 4. Try to move forward now
        if move_rover(dx, dy):
            pass  # We successfully moved forward!
        else:
            # 5. We are blocked on the right and in front. Turn left.
            turn_left()

    # --- End of your code ---

    algorithm_steps += 1


def random_mouse_step():
    """Perform one step of the random mouse maze solving algorithm."""
    global algorithm_steps
    import random
    
    # Get all possible directions we can move
    valid_directions = []
    
    for direction_index in range(4):  # Check all 4 directions
        dx, dy = directions[direction_index]
        new_x = rover_x + dx
        new_y = rover_y + dy
        
        # Check if this direction is valid (not a wall)
        if can_move(new_x, new_y):
            valid_directions.append(direction_index)
    
    if not valid_directions:
        # If we're completely stuck, just turn in place
        turn_right()
        algorithm_steps += 1
        return
    
    # Smart random selection: prefer directions that don't go backwards
    preferred_directions = []
    backwards_direction = (rover_direction + 2) % 4  # Opposite of current direction
    
    for direction in valid_directions:
        if direction != backwards_direction:
            preferred_directions.append(direction)
    
    # Choose direction: prefer non-backwards moves, but allow backwards if that's all we have
    if preferred_directions:
        chosen_direction = random.choice(preferred_directions)
    else:
        chosen_direction = random.choice(valid_directions)
    
    # Turn to face the chosen direction
    while rover_direction != chosen_direction:
        turn_right()
    
    # Move in the chosen direction
    dx, dy = directions[rover_direction]
    move_rover(dx, dy)
    
    algorithm_steps += 1


# ==============================================================================
#  BELOW THIS LINE IS THE GAME ENGINE AND DRAWING CODE.
#  You don't need to change anything here for the workshop.
# ==============================================================================
def draw_map():
    """Draw the map with moon background and rock sprites"""
    # Draw mars background first
    screen.blit(mars_background, (0, UI_HEIGHT))
    # Create a semi-transparent surface for the boundary walls
    boundary_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # Fill it with a semi-transparent gray color (R, G, B, Alpha)
    # Alpha = 0 is fully transparent, 255 is fully opaque.
    boundary_tile.fill((100, 100, 120, 128))  # 128 is about 50% transparent

    # Draw grid lines
    for x in range(0, WINDOW_WIDTH + 1, TILE_SIZE):
        pygame.draw.line(screen, (100, 100, 120), (x, UI_HEIGHT),
                         (x, WINDOW_HEIGHT), 1)
    for y in range(UI_HEIGHT, WINDOW_HEIGHT + 1, TILE_SIZE):
        pygame.draw.line(screen, (100, 100, 120), (0, y), (WINDOW_WIDTH, y), 1)

    # Draw rocks (walls) but skip boundary walls (make them invisible)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if map[y][x] == 1:  # Wall
                # Skip drawing boundary walls (make them invisible)
                if (x == 0 or x == MAP_WIDTH - 1 or y == 0
                        or y == MAP_HEIGHT - 1):
                    screen.blit(boundary_tile,
                                (x * TILE_SIZE, y * TILE_SIZE + UI_HEIGHT))

                else:
                    rect = pygame.Rect(x * TILE_SIZE,
                                       y * TILE_SIZE + UI_HEIGHT, TILE_SIZE,
                                       TILE_SIZE)
                    screen.blit(obstacle_sprite, rect)


def draw_rover_and_goal():
    """Draw rover with rotation, goal, and trail"""
    # Draw trail
    for trail_x, trail_y in rover_trail:
        trail_rect = pygame.Rect(trail_x * TILE_SIZE + 15,
                                 trail_y * TILE_SIZE + 15 + UI_HEIGHT, 10, 10)
        pygame.draw.rect(screen, BLUE, trail_rect)

    # Draw goal
    goal_rect = pygame.Rect(goal_x * TILE_SIZE, goal_y * TILE_SIZE + UI_HEIGHT,
                            TILE_SIZE, TILE_SIZE)
    screen.blit(goal_sprite, goal_rect)

    # Draw rover with rotation
    rover_rect = pygame.Rect(rover_x * TILE_SIZE + 2,
                             rover_y * TILE_SIZE + UI_HEIGHT + 2,
                             TILE_SIZE - 4, TILE_SIZE - 4)

    screen.blit(player_sprite, rover_rect)


def draw_ui():
    """Draw user interface in the top bar"""
    # Draw UI background
    ui_rect = pygame.Rect(0, 0, WINDOW_WIDTH, UI_HEIGHT)
    pygame.draw.rect(screen, (40, 40, 40), ui_rect)
    pygame.draw.line(screen, WHITE, (0, UI_HEIGHT), (WINDOW_WIDTH, UI_HEIGHT),
                     2)

    if drawing_mode:
        text1 = font.render("DRAWING MODE", True, YELLOW)
        screen.blit(text1, (10, 10))
        text2 = font.render(
            "Click/drag: Draw rocks | Right-click: Erase | ENTER: Start game",
            True, WHITE)
        screen.blit(text2, (10, 35))
        text3 = font.render("E: Empty map | M: Default map", True, WHITE)
        screen.blit(text3, (10, 60))
    else:
        mode = "ALGORITHM RUNNING" if algorithm_running else "MANUAL MODE (Arrow Keys)"
        color = GREEN if algorithm_running else WHITE
        text1 = font.render(mode, True, color)
        screen.blit(text1, (10, 10))

        text2 = font.render(
            "SPACE: Toggle Algorithm | A: Switch Algorithm | R: Reset | E: Drawing mode", True,
            WHITE)
        screen.blit(text2, (10, 35))

        info = font.render(
            f"Pos: ({rover_x},{rover_y}) Dir: {direction_names[rover_direction]}",
            True, WHITE)
        screen.blit(info, (500, 10))
        
        algorithm_name = "Wall Follower" if current_algorithm == "wall_follower" else "Random Mouse"
        algorithm_text = font.render(f"Algorithm: {algorithm_name}", True, WHITE)
        screen.blit(algorithm_text, (500, 35))

        if algorithm_running:
            steps_text = font.render(f"Steps: {algorithm_steps}", True, WHITE)
            screen.blit(steps_text, (650, 60))

    if game_won:
        win_text = font.render("YOU ESCAPED THE CAVE!", True, GREEN)
        text_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2,
                                              WINDOW_HEIGHT // 2))
        pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 20))
        screen.blit(win_text, text_rect)


def reset_game():
    """Reset the rover to start position"""
    global rover_x, rover_y, rover_direction, rover_trail, game_won, algorithm_running, algorithm_steps, current_algorithm
    rover_x = 1
    rover_y = 1
    rover_direction = 0
    rover_trail = []
    game_won = False
    algorithm_running = False
    algorithm_steps = 0
    # Keep the current_algorithm setting - don't reset it so user can keep their preference


# Main game loop
running = True
last_algorithm_time = 0

while running:
    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if drawing_mode:
                if event.key == pygame.K_RETURN:  # Enter key
                    drawing_mode = False
                elif event.key == pygame.K_e:  # E key - empty map
                    create_empty_map()
                    reset_game()
                elif event.key == pygame.K_m:  # M key - default map
                    create_default_map()
                    reset_game()
            else:
                # Manual rover controls
                if not algorithm_running:
                    if event.key == pygame.K_UP:  # Up
                        rover_direction = 0
                        move_rover(0, -1)
                    elif event.key == pygame.K_DOWN:  # Down
                        rover_direction = 2
                        move_rover(0, 1)
                    elif event.key == pygame.K_LEFT:  # Left
                        rover_direction = 3
                        move_rover(-1, 0)
                    elif event.key == pygame.K_RIGHT:  # Right
                        rover_direction = 1
                        move_rover(1, 0)

                # Algorithm controls
                if event.key == pygame.K_SPACE:
                    algorithm_running = not algorithm_running
                
                # Switch algorithm
                if event.key == pygame.K_a:
                    if current_algorithm == "wall_follower":
                        current_algorithm = "random_mouse"
                    else:
                        current_algorithm = "wall_follower"
                    algorithm_steps = 0  # Reset step counter when switching algorithms

                # Reset
                if event.key == pygame.K_r:
                    reset_game()

                # Go back to drawing mode
                if event.key == pygame.K_e:
                    drawing_mode = True

        # Mouse drawing
        elif event.type == pygame.MOUSEBUTTONDOWN and drawing_mode:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Adjust for UI bar
            if mouse_y >= UI_HEIGHT:
                grid_x = mouse_x // TILE_SIZE
                grid_y = (mouse_y - UI_HEIGHT) // TILE_SIZE

                if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
                    # Don't allow drawing on boundary cells or start/goal positions
                    if (grid_x == 0 or grid_x == MAP_WIDTH - 1 or grid_y == 0
                            or grid_y == MAP_HEIGHT - 1
                            or (grid_x == 1 and grid_y == 1)
                            or  # Start position
                        (grid_x == goal_x
                         and grid_y == goal_y)):  # Goal position
                        continue

                    if event.button == 1:  # Left click - draw wall
                        map[grid_y][grid_x] = 1
                    elif event.button == 3:  # Right click - erase wall
                        map[grid_y][grid_x] = 0

    # Mouse dragging for drawing
    if drawing_mode and pygame.mouse.get_pressed()[0]:  # Left mouse held
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y >= UI_HEIGHT:
            grid_x = mouse_x // TILE_SIZE
            grid_y = (mouse_y - UI_HEIGHT) // TILE_SIZE
            if (0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT
                    and not (grid_x == 0 or grid_x == MAP_WIDTH - 1
                             or grid_y == 0 or grid_y == MAP_HEIGHT - 1 or
                             (grid_x == 1 and grid_y == 1) or
                             (grid_x == goal_x and grid_y == goal_y))):
                map[grid_y][grid_x] = 1

    if drawing_mode and pygame.mouse.get_pressed()[2]:  # Right mouse held
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y >= UI_HEIGHT:
            grid_x = mouse_x // TILE_SIZE
            grid_y = (mouse_y - UI_HEIGHT) // TILE_SIZE
            if (0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT
                    and not (grid_x == 0 or grid_x == MAP_WIDTH - 1
                             or grid_y == 0 or grid_y == MAP_HEIGHT - 1)):
                map[grid_y][grid_x] = 0

    # Run algorithm
    if algorithm_running and not game_won and current_time - last_algorithm_time > 200:
        if current_algorithm == "wall_follower":
            wall_follower_step()
        else:  # random_mouse
            random_mouse_step()
        last_algorithm_time = current_time

    # Check win condition
    if rover_x == goal_x and rover_y == goal_y:
        game_won = True
        algorithm_running = False

    # Draw everything
    screen.fill(BLACK)
    draw_map()
    if not drawing_mode:
        draw_rover_and_goal()
    draw_ui()

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
