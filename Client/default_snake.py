# The default snake the program uses so the users can play with their snakes and check them
# This file's structure is similar to your_snake.py's structure, but it also includes the way the demo-snake should move

def think(apple_location : tuple, snake_head : tuple, snake_length, snake_direction : tuple):
    UP = (0,1)
    DOWN = (0,-1)
    LEFT = (-1,0)
    RIGHT = (1,0)
    output = (0,0)
    if(snake_head[0] < apple_location[0] and snake_direction != LEFT):
        output = RIGHT
    elif(snake_head[0] > apple_location[0] and snake_direction != RIGHT):
        output = LEFT
    elif(snake_head[1] < apple_location[1] and snake_direction != DOWN):
        output = UP
    elif(snake_head[1] > apple_location[1] and snake_direction != UP):
        output = DOWN
    else:
        output = snake_direction
    return output
