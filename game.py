import pygame
import sys
import random
import time
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 400
SQUARE_X = (WIDTH - SQUARE_SIZE) // 2
SQUARE_Y = (HEIGHT - SQUARE_SIZE) // 2
GRID_SIZE = 20
GRID_WIDTH = SQUARE_SIZE // GRID_SIZE
GRID_HEIGHT = SQUARE_SIZE // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Impossible Snake Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("comicsansms", 35)
small_font = pygame.font.SysFont("comicsansms", 25)

# Global background variable
jungle_bg = None

# Load jungle background
def load_jungle_bg():
    global jungle_bg
    try:
        # Try different possible file locations
        file_locations = ["jungle.png", "assets/jungle.png", "../jungle.png", "./jungle.png"]
        for file_path in file_locations:
            if os.path.exists(file_path):
                jungle_bg = pygame.image.load(file_path)
                jungle_bg = pygame.transform.scale(jungle_bg, (WIDTH, HEIGHT))
                print(f"Successfully loaded jungle background from {file_path}")
                return True
        
        # If we got here, no file was found
        print("WARNING: jungle.png not found in any expected location.")
        return False
    except Exception as e:
        print(f"Error loading jungle background: {e}")
        return False

# Load background at startup
load_jungle_bg()

class Game:
    def __init__(self):
        self.running = True
        self.game_over = False
        self.game_started = False
        self.start_time = 0
        self.last_food_time = 0
        self.score = 0
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.snake_pos = [SQUARE_X + SQUARE_SIZE // 2, SQUARE_Y + SQUARE_SIZE // 2]
        self.snake_body = [[SQUARE_X + SQUARE_SIZE // 2, SQUARE_Y + SQUARE_SIZE // 2],
                          [SQUARE_X + SQUARE_SIZE // 2 - GRID_SIZE, SQUARE_Y + SQUARE_SIZE // 2],
                          [SQUARE_X + SQUARE_SIZE // 2 - (2 * GRID_SIZE), SQUARE_Y + SQUARE_SIZE // 2]]
        self.food_pos = self.spawn_food()
        
        # Create default background (jungle-like gradient)
        self.background = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            green_val = int(100 + (y / HEIGHT) * 80)
            pygame.draw.line(self.background, (0, green_val, 0), (0, y), (WIDTH, y))
    
    def reset_game(self):
        """Reset the game state without showing the start screen"""
        self.game_over = False
        self.start_time = time.time()
        self.last_food_time = time.time()
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.snake_pos = [SQUARE_X + SQUARE_SIZE // 2, SQUARE_Y + SQUARE_SIZE // 2]
        self.snake_body = [[SQUARE_X + SQUARE_SIZE // 2, SQUARE_Y + SQUARE_SIZE // 2],
                          [SQUARE_X + SQUARE_SIZE // 2 - GRID_SIZE, SQUARE_Y + SQUARE_SIZE // 2],
                          [SQUARE_X + SQUARE_SIZE // 2 - (2 * GRID_SIZE), SQUARE_Y + SQUARE_SIZE // 2]]
        self.food_pos = self.spawn_food()
    
    def spawn_food(self):
        # Spawn food within the square boundaries
        return [random.randrange(SQUARE_X + GRID_SIZE, SQUARE_X + SQUARE_SIZE - GRID_SIZE, GRID_SIZE),
                random.randrange(SQUARE_Y + GRID_SIZE, SQUARE_Y + SQUARE_SIZE - GRID_SIZE, GRID_SIZE)]
    
    def show_start_screen(self):
        # Draw background
        if jungle_bg:
            screen.blit(jungle_bg, (0, 0))
        else:
            screen.blit(self.background, (0, 0))
        
        # Draw title and button
        title = font.render("JUST WIN", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        
        # Draw button
        button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
        pygame.draw.rect(screen, GREEN, button_rect)
        
        # Button text
        button_text = small_font.render("START", True, BLACK)
        screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 10))
        
        pygame.display.flip()
        
        # Wait for button click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        waiting = False
                        self.game_started = True
                        self.start_time = time.time()
                        self.last_food_time = time.time()
    
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.change_to = "DOWN"
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.change_to = "LEFT"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.change_to = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE and self.game_over:
                    # Just reset the game state without showing start screen
                    self.reset_game()
    
    def move_snake(self):
        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        if self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
        
        # Moving the snake
        if self.direction == "UP":
            self.snake_pos[1] -= GRID_SIZE
        if self.direction == "DOWN":
            self.snake_pos[1] += GRID_SIZE
        if self.direction == "LEFT":
            self.snake_pos[0] -= GRID_SIZE
        if self.direction == "RIGHT":
            self.snake_pos[0] += GRID_SIZE
        
        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_pos))
        self.snake_body.pop()
    
    def check_collision(self):
        # Check if snake is out of the square boundaries
        if (self.snake_pos[0] < SQUARE_X or self.snake_pos[0] >= SQUARE_X + SQUARE_SIZE or
            self.snake_pos[1] < SQUARE_Y or self.snake_pos[1] >= SQUARE_Y + SQUARE_SIZE):
            self.game_over = True
            return True
        
        # Check if snake collides with itself
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over = True
                return True
        
        # Check if snake eats food - this is designed to kill the player (impossible condition)
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.game_over = True
            return True
        
        # Check if 10 seconds passed without eating food
        if time.time() - self.last_food_time > 10:
            self.game_over = True
            return True
        
        # Check if player survived for 15 seconds (impossible condition)
        if time.time() - self.start_time > 15:
            # This is theoretically the win condition, but it's impossible to reach
            # because you die at 10 seconds without eating food and die if you eat food
            self.game_over = True
            return True
        
        return False
    
    def show_game_over_screen(self):
        # Draw background
        if jungle_bg:
            screen.blit(jungle_bg, (0, 0))
        else:
            screen.blit(self.background, (0, 0))
            
        # Game over text and messages
        game_over_text = font.render("GAME OVER", True, RED)
        restart_text = small_font.render("Press SPACE to try again", True, WHITE)
        impossible_text1 = font.render("NICE TRY!", True, WHITE)
        impossible_text2 = small_font.render("This game is designed to be IMPOSSIBLE to win!", True, WHITE)
        
        # Draw restart button
        button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 70, 150, 50)
        pygame.draw.rect(screen, GREEN, button_rect)
        button_text = small_font.render("RESTART", True, BLACK)
        
        # Position all elements
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - 50))
        screen.blit(impossible_text1, (WIDTH // 2 - impossible_text1.get_width() // 2, HEIGHT // 3))
        screen.blit(impossible_text2, (WIDTH // 2 - impossible_text2.get_width() // 2, HEIGHT // 3 + 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))
        screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 80))
        
        pygame.display.flip()
        
        # Handle restart button click
        waiting = True
        while waiting and self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Just reset the game state without showing start screen
                        self.reset_game()
                        waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        # Just reset the game state without showing start screen
                        self.reset_game()
                        waiting = False
    
    def draw_elements(self):
        # Draw background
        if jungle_bg:
            screen.blit(jungle_bg, (0, 0))
        else:
            screen.blit(self.background, (0, 0))
        
        # Draw the square playing area
        pygame.draw.rect(screen, GRAY, (SQUARE_X, SQUARE_Y, SQUARE_SIZE, SQUARE_SIZE), 2)
        
        # Draw snake
        for pos in self.snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))
        
        # Draw food (red circle)
        pygame.draw.circle(screen, RED, (self.food_pos[0] + GRID_SIZE // 2, self.food_pos[1] + GRID_SIZE // 2), GRID_SIZE // 2)
        
        # Timer
        elapsed_time = time.time() - self.start_time
        time_left = max(0, 15 - elapsed_time)
        timer_text = small_font.render(f"Time: {elapsed_time:.1f}/15.0", True, WHITE)
        food_timer_text = small_font.render(f"Food Timer: {max(0, 10 - (time.time() - self.last_food_time)):.1f}/10.0", True, WHITE)
        taunt_text = small_font.render("We dare you to win and survive 15 SEC", True, WHITE)
        
        screen.blit(timer_text, (10, 10))
        screen.blit(food_timer_text, (10, 40))
        screen.blit(taunt_text, (WIDTH - taunt_text.get_width() - 10, 10))
    
    def run(self):
        # Only show start screen at the beginning
        self.show_start_screen()
        
        while self.running:
            if not self.game_over:
                self.handle_keys()
                self.move_snake()
                self.check_collision()
                self.draw_elements()
                pygame.display.flip()
                clock.tick(FPS)
            else:
                self.show_game_over_screen()

# Add detailed instructions to the console
print("==== Impossible Snake Game ====")
print("IMPORTANT: Make sure jungle.png is in the same folder as this script!")
print("If the jungle background isn't showing up, here's what to try:")
print("1. Create a file named exactly 'jungle.png' in the same folder as this script")
print("2. Make sure the image is a valid PNG file")
print("3. Try placing the image in an 'assets' folder")
print("Controls: Arrow keys or WASD to move")
print("Press SPACE or click RESTART to immediately restart after game over")

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()