import pygame
import sys
import random

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
SNAKE_SIZE = 20
FPS = 10

# Colors.
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Direction vectors.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class.
class Snake:
    def __init__(self, starting_pos : tuple, color : tuple, ):
        self.length = 1
        self.positions = [starting_pos]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = color
        self.is_alive = True
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self, other_snake_pos : [tuple]):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:] or new in other_snake_pos:
            self.reset()
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.is_alive = False
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], SNAKE_SIZE, SNAKE_SIZE))
    
    def get_score(self):
        return self.score


# Food class.
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], SNAKE_SIZE, SNAKE_SIZE))


# Superfood class.
class Superfood():
    def __init__(self):
        self.position = (0,0)
        self.color = BLACK
        self.is_hidden = True
    
    def set_food_color(self, color):
        self.color = color
        
    def hide(self):
        self.position = (0,0)
        self.is_hidden = True
        self.color = BLACK
    
    def uncover(self):
        self.color = WHITE
        self.is_hidden = False    
        self.randomize_position()

    def randomize_position(self):
         self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                          random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], SNAKE_SIZE, SNAKE_SIZE))
