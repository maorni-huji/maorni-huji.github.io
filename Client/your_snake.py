import classes
#Your very own snake!
#Returns the direction the snake will be facing.
def think(food : classes.Food, superfood: classes.Superfood, this_snake : classes.Snake, other_snake: classes.Snake):
    UP = (0,1)
    DOWN = (0,-1)
    LEFT = (-1,0)
    RIGHT = (1,0)
    output = (0,0)
    return output