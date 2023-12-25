#The actual snake game that utilises the brains provided by the two players.
import pygame
import sys
import random
import default_snake
import classes

#Initialize Pygame.
pygame.init()

#Constants.
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
SNAKE_SIZE = 20
FPS = 10

#Colors.
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def main():
    #Initializing all the objects required for pygame.
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    frame = 1

    #Initializing the game objects.
    blue_snake = classes.Snake((60,60), BLUE)
    green_snake = classes.Snake((540,540), GREEN)
    food = classes.Food()
    superfood = classes.Superfood()
    run = True
    
    #Running the game.
    while run:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        #Replace "default_snake" with your own snake bot file, remember to also import your file at the top of this file!
        blue_snake.direction = default_snake.think(food, superfood, blue_snake, green_snake)
        green_snake.direction = default_snake.think(food, superfood, green_snake, blue_snake)

        #Checking to see both snakes are still alive.
        blue_positions = blue_snake.positions
        run = blue_snake.update(green_snake.positions) and green_snake.update(blue_positions)
        
        #Checking to see if a snake ate an apple.
        if blue_snake.get_head_position() == food.position:
            blue_snake.length += 1
            blue_snake.score += 1
            food.randomize_position()
        elif green_snake.get_head_position() == food.position:
            green_snake.length += 1
            green_snake.score += 1
            food.randomize_position()
            
        #Checking to see if a snake ate the superfood.
        if blue_snake.get_head_position() == superfood.position and superfood.is_hidden == False:
            blue_snake.length += 5
            blue_snake.score += 5
            frame = 0
            superfood.hide()    
        elif green_snake.get_head_position() == superfood.position and superfood.is_hidden == False:
            green_snake.length += 5
            green_snake.score += 5
            frame = 0
            superfood.hide()
            
        #Creating a new superfood.
        if frame%100 == 0 and superfood.is_hidden == True:
            frame = 1
            superfood.uncover()
        
        #Destroying the superfood if too much time has passed.
        if frame%50 == 0 and superfood.is_hidden == False:
            frame = 1
            superfood.hide()
        
        #Rendering everything to the screen.
        if run:
            surface.fill(BLACK)
            blue_snake.render(surface)
            green_snake.render(surface)
            food.render(surface)
            superfood.render(surface)
            screen.blit(surface, (0, 0))
            pygame.display.update()
        clock.tick(FPS)
    
    #Adding up the final scores, a bonus is given if your snake stays alive.
    if(blue_snake.is_alive):
        blue_snake.score += 20
    if(green_snake.is_alive):
        green_snake.score += 20
        
    #Displaying the scores.
    font = pygame.font.Font(None, 36)
    # Create a text surface
    blue_text = "The blue snakes score is: " + str(blue_snake.score)
    blue_text_surface = font.render(blue_text, True, BLUE)
    green_text = "The green snakes score is: " + str(green_snake.score)
    green_text_surface = font.render(green_text, True, GREEN)

    # Get the rectangle of the text surface
    text_rect = blue_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rect2 = green_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(blue_text_surface, text_rect)
        screen.blit(green_text_surface, text_rect2)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
