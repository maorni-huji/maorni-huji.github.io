import classes
from classes import RIGHT, LEFT, UP, DOWN  # directions

#Your very own snake!
#Returns the direction the snake will be facing.
def think(food : classes.Food, superfood: classes.Superfood, this_snake : classes.Snake, other_snake: classes.Snake):
    UP = (0,1)
    DOWN = (0,-1)
    LEFT = (-1,0)
    RIGHT = (1,0)

    if other_snake.length % 2 == 0:  # just an example of a stupid snake, edit your own code!
        output = LEFT
    else:
        output = DOWN
    return output


