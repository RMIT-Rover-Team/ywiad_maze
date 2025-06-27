import pygame
import math
import numpy as np
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TILE_SIZE = 32
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Directions for wall following
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
DIRECTION_NAMES = ["UP", "RIGHT", "DOWN", "LEFT"]

class CaveEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = np.zeros((height, width), dtype=int)
        self.tile_sprites = {}
        self.load_tileset()
        self.generate_cave()
    
    def load_tileset(self):
        """Load and prepare cave tileset"""
        try:
            # Try to load the cave tileset
            if os.path.exists("assets/cave.png"):
                tileset_image = pygame.image.load("assets/cave.png")
            else:
                # Create a simple tileset if file doesn't exist
                tileset_image = pygame.Surface((256, 256))
                tileset_image.fill((139, 69, 19))  # Brown for walls
        except:
            # Fallback: create simple colored tiles
            tileset_image = pygame.Surface((256, 256))
            tileset_image.fill((139, 69, 19))
        
        # Extract individual tiles (assuming 8x8 grid of 32x32 tiles)
        tile_width = tile_height = 32
        for row in range(8):
            for col in range(8):
                tile_id = row * 8 + col
                x = col * tile_width
                y = row * tile_height
                
                if x + tile_width <= tileset_image.get_width() and y + tile_height <= tileset_image.get_height():
                    tile_surface = pygame.Surface((tile_width, tile_height))
                    tile_surface.blit(tileset_image, (0, 0), (x, y, tile_width, tile_height))
                else:
                    # Create colored tiles as fallback
                    tile_surface = pygame.Surface((tile_width, tile_height))
                    if tile_id == 0:  # Empty space
                        tile_surface.fill(BLACK)
                    else:  # Wall
                        tile_surface.fill((139, 69, 19))  # Brown
                
                self.tile_sprites[tile_id] = tile_surface
    
    def generate_cave(self):
        """Generate a simple cave layout"""
        # Create walls around the border
        for x in range(self.width):
            self.tiles[0][x] = 1  # Top wall
            self.tiles[self.height-1][x] = 1  # Bottom wall
        
        for y in range(self.height):
            self.tiles[y][0] = 1  # Left wall
            self.tiles[y][self.width-1] = 1  # Right wall
        
        # Create some internal walls to make it interesting
        # Horizontal walls
        for x in range(5, 15):
            self.tiles[5][x] = 1
            self.tiles[15][x] = 1
        
        # Vertical walls
        for y in range(3, 8):
            self.tiles[y][20] = 1
            self.tiles[y][25] = 1
        
        # Create a maze-like structure
        for y in range(8, 12):
            for x in range(8, 12):
                if (x + y) % 3 == 0:
                    self.tiles[y][x] = 1
        
        # Add some scattered obstacles
        obstacles = [(10, 18), (15, 20), (8, 25), (18, 8), (22, 15)]
        for x, y in obstacles:
            if 0 < x < self.width-1 and 0 < y < self.height-1:
                self.tiles[y][x] = 1
    
    def is_wall(self, x, y):
        """Check if a position is a wall"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.tiles[y][x] != 0
    
    def get_tile_at_pixel(self, pixel_x, pixel_y):
        """Convert pixel coordinates to tile coordinates"""
        tile_x = pixel_x // TILE_SIZE
        tile_y = pixel_y // TILE_SIZE
        return tile_x, tile_y
    
    def render(self, screen):
        """Render the cave environment"""
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.tiles[y][x]
                if tile_id in self.tile_sprites:
                    screen.blit(self.tile_sprites[tile_id], (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    # Fallback rendering
                    color = BLACK if tile_id == 0 else (139, 69, 19)
                    pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

class LunarRover:
    def __init__(self, x, y, cave_env):
        self.x = float(x)
        self.y = float(y)
        self.angle = 0  # Facing direction in degrees
        self.speed = 2.0
        self.rotation_speed = 3.0
        self.cave_env = cave_env
        self.sprite = None
        self.load_sprite()
        
        # Wall following algorithm state
        self.following_wall = False
        self.wall_direction = 1  # 0=Up, 1=Right, 2=Down, 3=Left
        self.last_wall_contact = None
        
    def load_sprite(self):
        """Load and prepare rover sprite"""
        try:
            if os.path.exists("assets/rover.png"):
                self.sprite = pygame.image.load("assets/rover.png")
            else:
                # Create a simple rover sprite
                self.sprite = pygame.Surface((24, 24), pygame.SRCALPHA)
                pygame.draw.polygon(self.sprite, WHITE, [(12, 0), (24, 24), (12, 18), (0, 24)])
                pygame.draw.circle(self.sprite, RED, (12, 12), 3)
        except:
            # Fallback sprite
            self.sprite = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.polygon(self.sprite, WHITE, [(12, 0), (24, 24), (12, 18), (0, 24)])
            pygame.draw.circle(self.sprite, RED, (12, 12), 3)
    
    def update_manual(self, keys):
        """Update rover position based on manual controls"""
        if not self.following_wall:
            # Rotation
            if keys[pygame.K_a]:
                self.angle -= self.rotation_speed
            if keys[pygame.K_d]:
                self.angle += self.rotation_speed
            
            # Movement
            if keys[pygame.K_w]:
                self.move_forward()
            if keys[pygame.K_s]:
                self.move_backward()
    
    def move_forward(self):
        """Move rover forward in the direction it's facing"""
        rad = math.radians(self.angle)
        new_x = self.x + math.cos(rad) * self.speed
        new_y = self.y + math.sin(rad) * self.speed
        
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
    
    def move_backward(self):
        """Move rover backward"""
        rad = math.radians(self.angle)
        new_x = self.x - math.cos(rad) * self.speed
        new_y = self.y - math.sin(rad) * self.speed
        
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
    
    def check_collision(self, x, y):
        """Check if the rover would collide with walls at the given position"""
        # Check corners of the rover
        rover_size = 12  # Half the rover size
        corners = [
            (x - rover_size, y - rover_size),
            (x + rover_size, y - rover_size),
            (x - rover_size, y + rover_size),
            (x + rover_size, y + rover_size)
        ]
        
        for corner_x, corner_y in corners:
            tile_x, tile_y = self.cave_env.get_tile_at_pixel(corner_x, corner_y)
            if self.cave_env.is_wall(tile_x, tile_y):
                return True
        return False
    
    def update_wall_following(self):
        """Update rover using wall following algorithm (right-hand rule)"""
        if not self.following_wall:
            return
        
        # Convert current position to tile coordinates
        tile_x, tile_y = self.cave_env.get_tile_at_pixel(self.x, self.y)
        
        # Right-hand rule wall following
        # 1. Try to turn right and move
        # 2. If can't, try to move forward
        # 3. If can't, try to turn left
        # 4. If can't, turn around
        
        right_dir = (self.wall_direction + 1) % 4
        forward_dir = self.wall_direction
        left_dir = (self.wall_direction - 1) % 4
        back_dir = (self.wall_direction + 2) % 4
        
        # Check each direction
        directions_to_try = [right_dir, forward_dir, left_dir, back_dir]
        
        for direction in directions_to_try:
            dx, dy = DIRECTIONS[direction]
            next_tile_x = tile_x + dx
            next_tile_y = tile_y + dy
            
            if not self.cave_env.is_wall(next_tile_x, next_tile_y):
                # Move in this direction
                self.wall_direction = direction
                self.angle = direction * 90  # Update visual direction
                
                # Move toward the center of the target tile
                target_x = next_tile_x * TILE_SIZE + TILE_SIZE // 2
                target_y = next_tile_y * TILE_SIZE + TILE_SIZE // 2
                
                # Smooth movement toward target
                dx_move = target_x - self.x
                dy_move = target_y - self.y
                distance = math.sqrt(dx_move * dx_move + dy_move * dy_move)
                
                if distance > 1:
                    move_speed = min(self.speed, distance)
                    self.x += (dx_move / distance) * move_speed
                    self.y += (dy_move / distance) * move_speed
                
                break
    
    def toggle_wall_following(self):
        """Toggle between manual control and wall following mode"""
        self.following_wall = not self.following_wall
        if self.following_wall:
            # Initialize wall following state
            tile_x, tile_y = self.cave_env.get_tile_at_pixel(self.x, self.y)
            
            # Find the best initial direction (look for a wall to follow)
            for i, (dx, dy) in enumerate(DIRECTIONS):
                if self.cave_env.is_wall(tile_x + dx, tile_y + dy):
                    self.wall_direction = (i + 1) % 4  # Turn right from wall
                    break
    
    def render(self, screen):
        """Render the rover"""
        if self.sprite:
            # Rotate sprite based on current angle
            rotated_sprite = pygame.transform.rotate(self.sprite, -self.angle)
            sprite_rect = rotated_sprite.get_rect(center=(self.x, self.y))
            screen.blit(rotated_sprite, sprite_rect)
            
            # Draw direction indicator
            if self.following_wall:
                # Draw a green circle to indicate autonomous mode
                pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 20, 3)
            else:
                # Draw a blue circle for manual mode
                pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 20, 3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lunar Rover Cave Navigation")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create cave environment
        cave_width = SCREEN_WIDTH // TILE_SIZE
        cave_height = SCREEN_HEIGHT // TILE_SIZE
        self.cave = CaveEnvironment(cave_width, cave_height)
        
        # Create rover
        start_x = 3 * TILE_SIZE + TILE_SIZE // 2
        start_y = 3 * TILE_SIZE + TILE_SIZE // 2
        self.rover = LunarRover(start_x, start_y, self.cave)
        
        # Game state
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.rover.toggle_wall_following()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update game state"""
        keys = pygame.key.get_pressed()
        
        if self.rover.following_wall:
            self.rover.update_wall_following()
        else:
            self.rover.update_manual(keys)
    
    def render(self):
        """Render the game"""
        self.screen.fill(BLACK)
        
        # Render cave
        self.cave.render(self.screen)
        
        # Render rover
        self.rover.render(self.screen)
        
        # Render UI
        self.render_ui()
        
        pygame.display.flip()
    
    def render_ui(self):
        """Render user interface"""
        # Control mode indicator
        mode_text = "AUTONOMOUS (Wall Following)" if self.rover.following_wall else "MANUAL (WASD)"
        mode_color = GREEN if self.rover.following_wall else BLUE
        mode_surface = self.font.render(mode_text, True, mode_color)
        self.screen.blit(mode_surface, (10, 10))
        
        # Instructions
        instructions = [
            "WASD: Move rover (manual mode)",
            "SPACE: Toggle autonomous/manual mode",
            "ESC: Exit"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text_surface, (10, 50 + i * 25))
        
        # Rover position info
        pos_text = f"Position: ({int(self.rover.x)}, {int(self.rover.y)})"
        pos_surface = self.small_font.render(pos_text, True, WHITE)
        self.screen.blit(pos_surface, (10, SCREEN_HEIGHT - 60))
        
        angle_text = f"Angle: {int(self.rover.angle)}°"
        angle_surface = self.small_font.render(angle_text, True, WHITE)
        self.screen.blit(angle_surface, (10, SCREEN_HEIGHT - 35))
        
        if self.rover.following_wall:
            dir_text = f"Direction: {DIRECTION_NAMES[self.rover.wall_direction]}"
            dir_surface = self.small_font.render(dir_text, True, GREEN)
            self.screen.blit(dir_surface, (10, SCREEN_HEIGHT - 10))
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Create placeholder asset files if they don't exist
def create_placeholder_assets():
    """Create placeholder asset files"""
    os.makedirs("assets", exist_ok=True)
    
    # Create placeholder cave tileset
    if not os.path.exists("assets/cave.png"):
        cave_surface = pygame.Surface((256, 256))
        # Create a simple pattern
        for y in range(0, 256, 32):
            for x in range(0, 256, 32):
                color = (139, 69, 19) if (x//32 + y//32) % 2 == 0 else (101, 67, 33)
                pygame.draw.rect(cave_surface, color, (x, y, 32, 32))
        pygame.image.save(cave_surface, "assets/cave.png")
    
    # Create placeholder rover sprite
    if not os.path.exists("assets/rover.png"):
        rover_surface = pygame.Surface((24, 24), pygame.SRCALPHA)
        # Draw a simple rover shape
        pygame.draw.polygon(rover_surface, (200, 200, 200), [(12, 2), (22, 22), (12, 18), (2, 22)])
        pygame.draw.circle(rover_surface, (255, 0, 0), (12, 12), 3)
        pygame.draw.circle(rover_surface, (0, 0, 0), (8, 8), 2)
        pygame.draw.circle(rover_surface, (0, 0, 0), (16, 8), 2)
        pygame.image.save(rover_surface, "assets/rover.png")

if __name__ == "__main__":
    create_placeholder_assets()
    game = Game()
    game.run()
