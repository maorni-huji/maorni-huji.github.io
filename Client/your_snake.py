import classes
from classes import RIGHT, LEFT, UP, DOWN  # directions

#Your very own snake!
#Returns the direction the snake will be facing.
def think(food : classes.Food, superfood: classes.Superfood, this_snake : classes.Snake, other_snake: classes.Snake):
    output = UP
    return output