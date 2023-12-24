#The actual snake game that utilises the brains provided by the two players.
import pygame
import sys
import random
import default_snake

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
SNAKE_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Snake class
class Snake:
    def __init__(self, starting_pos : tuple, color : tuple):
        self.length = 1
        self.positions = [starting_pos]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = color

    def get_head_position(self):
        return self.positions[0]

    def update(self, other_snake_pos : [tuple]):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:] or new in other_snake_pos:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        run = False
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        return run

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], SNAKE_SIZE, SNAKE_SIZE))


# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def set_food_color(self, color):
        self.color = color

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], SNAKE_SIZE, SNAKE_SIZE))


# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake_1 = Snake((60,60), BLUE)
    snake_2 = Snake((540,540), GREEN)
    food = Food()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        snake_1.direction = default_snake.think(food.position, snake_1.get_head_position(), snake_1.length, snake_1.direction)
        snake_2.direction = default_snake.think(food.position, snake_2.get_head_position(), snake_2.length, snake_2.direction)


        run = snake_1.update(snake_2.positions)
        if (run == False):
            break
        run = snake_2.update(snake_1.positions)
        if (run == False):
            break
        if snake_1.get_head_position() == food.position:
            snake_1.length += 1
            food.randomize_position()
        elif snake_2.get_head_position() == food.position:
            snake_2.length += 1
            food.randomize_position()
        surface.fill(BLACK)
        snake_1.render(surface)
        snake_2.render(surface)
        food.render(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
