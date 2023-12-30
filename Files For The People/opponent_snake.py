# The default snake the program uses so the users can play with their snakes and check them
# This file's structure is similar to your_snake.py's structure, but it also includes the way the demo-snake should move

import classes
from classes import RIGHT, LEFT, UP, DOWN  # directions
import time

# Returns the direction vector your snake will move to. Output HAS TO BE one of UP, DOWN, LEFT, RIGHT.
def think(food : classes.Food, superfood: classes.Superfood, this_snake : classes.Snake, other_snake: classes.Snake):
    if this_snake.get_head_position()[0] < food.position[0] and this_snake.direction != LEFT:
        output = RIGHT
    elif this_snake.get_head_position()[0] > food.position[0] and this_snake.direction != RIGHT:
        output = LEFT
    elif this_snake.get_head_position()[1] < food.position[1] and this_snake.direction != DOWN:
        output = UP
    elif this_snake.get_head_position()[1] > food.position[1] and this_snake.direction != UP:
        output = DOWN
    else:
        output = this_snake.direction
    return output

