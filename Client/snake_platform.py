# The actual snake game that utilises the brains provided by the two players.
import pygame
import sys
import random
import classes
from classes import RIGHT, LEFT, UP, DOWN
import your_snake
import logging
import time

# TODO:
# 0. Can someone eat just one apple and kill himself, and this way to win the game? Is it ok for us?
# 1. Validate return values of the 'think' functions
# 2. Validate that the snake_platform.py file remains the same when running the game (with watermarks, for example)
# 3. Add a log file (using log library) that will save the actions of the game (for investigating it in case of a problem)
# 4. Add a button in the main gui that would ask the user for speed multiplication (x FPS)
# 5. In the main gui, write who is the blue snake and who is the green one
# 6. Bruker's offer - to add special modes?
# 7. Fix some code conventions (for PyCharm conventions)
# 8. In case of a tie, play another game
# 9. Write the score of each snake in the game while the game plays
# 10. Don't let the 'think' functions run for more than 0.1 seconds

# Initialize Pygame.
pygame.init()

# Constants.
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
SNAKE_SIZE = 20
FPS = 10
# Colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

HOST_WINS, OPPONENT_WINS = 0, 1

ALLOWED_DIRECTIONS = [UP, DOWN, LEFT, RIGHT, (1, 1), (1, -1), (-1, 1), (-1, -1)]


def run_snakes_game(is_real: bool = False):
    """
    Runs the Snake Game
    :param is_real: True for real competitors, False for trainings - using the default_snake file
    :return: The winner (HOST_WINS or OPPONENT_WINS);
    """
    your_think = your_snake.think  # your function!
    if is_real:
        import opponent_snake  # real opponent snake - do not touch!
        opponent_think = opponent_snake.think
    else:
        import \
            default_snake  # demo snake for training, you are allowed to edit default_snake.py for demonstrating possible opponents!
        opponent_think = default_snake.think

    # Initializing all the objects required for pygame.
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    superfood_timer = 1
    tick = 0

    # Initializing the game objects.
    blue_snake = classes.Snake((60, 60), BLUE)  # the host is the blue Snake, the opponent is the Green one
    green_snake = classes.Snake((540, 540), GREEN)
    food = classes.Food()
    superfood = classes.Superfood()
    run = True

    # Running the game.
    while run and (tick < 900 or blue_snake.score == green_snake.score):
        tick += 1
        superfood_timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        blue_food = green_food = classes.NO_APPLE

        # Letting the snakes make their next move.
        try:
            start = time.time()
            direction = your_think(food.copy(), superfood.copy(), blue_snake.copy(), green_snake.copy())
            end = time.time()
            if is_real:
                logging.info("host action time: " + str(end - start))
            if end - start >= 0.2:
                print("Took you long enough... MINUS A POINT TO GRIFFINDOR (a.k.a host)")
                blue_snake.score -= 1
            elif direction in ALLOWED_DIRECTIONS and direction != blue_snake.opposite_direction():
                blue_snake.direction = direction
            else:
                raise Exception("Host direction given isn't in allowed values")
        except Exception as e:
            print(f"Function raised an exception: {e}")

        try:
            start = time.time()
            direction = opponent_think(food.copy(), superfood.copy(), green_snake.copy(), blue_snake.copy())
            end = time.time()
            if is_real:
                logging.info("guest action time: " + str(end - start))
            if end - start >= 0.2:
                print("Took you long enough... MINUS A POINT TO GRIFFINDOR (a.k.a your guest)")
                green_snake.score -= 1
            elif direction in ALLOWED_DIRECTIONS and direction != green_snake.opposite_direction():
                green_snake.direction = direction
            else:
                raise Exception("Guest direction given isn't in allowed values")
        except Exception as e:
            print(f"Function raised an exception: {e}")

        # Checking to see both snakes are still alive.
        blue_copy = blue_snake.copy()
        blue_copy.update_just_positions(green_snake.positions)
        green_copy = green_snake.copy()
        green_copy.update_just_positions(blue_snake.positions)
        blue_run = blue_snake.update(green_copy.positions)
        green_run = green_snake.update(blue_copy.positions)
        run = blue_run and green_run
        # use the values in the correct time, tail-to-tail is ok

        # Checking to see if a snake ate an apple.
        if blue_snake.get_head_position() == food.position:
            blue_snake.length += 1
            blue_snake.score += 1
            food.randomize_position()
            blue_food = classes.RED_APPLE
        elif green_snake.get_head_position() == food.position:
            green_snake.length += 1
            green_snake.score += 1
            food.randomize_position()
            green_food = classes.RED_APPLE

        # Checking to see if a snake ate the superfood.
        if blue_snake.get_head_position() == superfood.position and superfood.is_hidden == False:
            blue_snake.length += 5
            blue_snake.score += 5
            superfood_timer = 0
            superfood.hide()
            blue_food = classes.SUPERFOOD
        elif green_snake.get_head_position() == superfood.position and superfood.is_hidden == False:
            green_snake.length += 5
            green_snake.score += 5
            superfood_timer = 0
            superfood.hide()
            green_food = classes.SUPERFOOD

        # Creating a new superfood.
        if superfood_timer % 100 == 0 and superfood.is_hidden == True:
            superfood_timer = 1
            superfood.uncover()

        # Destroying the superfood if too much time has passed.
        if superfood_timer % 50 == 0 and superfood.is_hidden == False:
            superfood_timer = 1
            superfood.hide()

        # log the actions to actions.log
        if is_real:
            log_actions(blue_snake.direction, green_snake.direction, blue_food, green_food, blue_snake.score,
                        green_snake.score)

        # Rendering everything to the screen.
        surface.fill(BLACK)
        blue_snake.render(surface)
        green_snake.render(surface)
        food.render(surface)
        superfood.render(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

    # Adding up the final scores, a bonus is given if your snake stays alive.
    if (blue_snake.is_alive):
        blue_snake.score += 20
    if (green_snake.is_alive):
        green_snake.score += 20

    # Displaying the scores.
    font = pygame.font.Font(None, 36)
    # Create a text surface
    blue_text = "The blue snakes score is: " + str(blue_snake.score)
    blue_text_surface = font.render(blue_text, True, BLUE)
    green_text = "The green snakes score is: " + str(green_snake.score)
    green_text_surface = font.render(green_text, True, GREEN)
    if blue_snake.score > green_snake.score:
        winner_text = "Host Won!"
        winner_text_surface = font.render(winner_text, True, BLUE)
    elif green_snake.score > blue_snake.score:
        winner_text = "Guest Won!"
        winner_text_surface = font.render(winner_text, True, GREEN)
    else:
        winner_text = "Draw... Play Again!"
        winner_text_surface = font.render(winner_text, True, WHITE)

    # log to file
    if is_real:
        logging.info("THE GAME IS DONE - Blue Snake Score: " + str(blue_snake.score) + ", Green Snake Score: " + str(
            green_snake.score) + "\n\n")

    # Get the rectangle of the text surface
    winner_text_rect = winner_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    text_rect = blue_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rect2 = green_text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
    start_time = time.time()
    while time.time() - start_time <= 3:
        screen.blit(winner_text_surface, winner_text_rect)
        screen.blit(blue_text_surface, text_rect)
        screen.blit(green_text_surface, text_rect2)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return HOST_WINS if blue_snake.score > green_snake.score else OPPONENT_WINS

    return HOST_WINS if blue_snake.score > green_snake.score else OPPONENT_WINS


def log_actions(blue_snake_dir: tuple[int, int], green_snake_dir: tuple[int, int],
                blue_food: int, green_food: int, blue_score: int, green_score: int):
    """
    Logs the current state to actions.log
    It should be called when the stage ends, and after the function logging.basicConfig was called (in main.py, run_game function)
    :param blue_snake_dir: The current step the blue snake has just done
    :param green_snake_dir: Same for the green snake
    :param blue_food: Whether the blue snake has eaten a red apple, a white apple or nothing at all (from  classes APPLES dictionary)
    :param green_food: Same for the green snake
    :param blue_score: The blue snake's current score
    :param green_score: Same for the green snake
    :return: None
    """
    logging.info(
        "Blue Direction: " + str(blue_snake_dir) + ", Blue Food: " + classes.APPLES[blue_food] + ", Blue Score: " + str(
            blue_score) + "\n"
                          "    Green Direction: " + str(green_snake_dir) + ", Green Food: " + classes.APPLES[
            green_food] + ", Green Score: " + str(green_score))