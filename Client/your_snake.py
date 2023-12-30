import classes
from classes import RIGHT, LEFT, UP, DOWN  # directions

"""
Your very own snake!
Receives a copy of the food, which grants you a point and makes you one unit longer.
Receives a copy of the superfood, which grants you 5 points, and makes you 5 units longer.
Receives your own snake, and receives to opponents snake.
Returns the direction the snake will be facing.
"""


def think(food: classes.Food, superfood: classes.Superfood, this_snake: classes.Snake, other_snake: classes.Snake):
    x_move = 0
    y_move = 0
    x_food = 0
    y_food = 0
    if superfood.is_hidden:
        x_food = food.position[0]
        y_food = food.position[1]
    else:
        x_food = superfood.position[0]
        y_food = superfood.position[1]

    if this_snake.get_head_position()[0] < x_food:
        if (x_food - this_snake.get_head_position()[0]) / 20 < (this_snake.get_head_position()[0] + 600 - x_food) / 20:
            x_move = 1
        else:
            x_move = -1
    elif this_snake.get_head_position()[0] > x_food:
        if (this_snake.get_head_position()[0] - x_food) / 20 < (600 - this_snake.get_head_position()[0] + x_food) / 20:
            x_move = -1
        else:
            x_move = 1
    if this_snake.get_head_position()[1] > y_food:
        if (this_snake.get_head_position()[1] - y_food) / 20 < (600 - this_snake.get_head_position()[1] + y_food) / 20:
            y_move = -1
        else:
            y_move = 1
    elif this_snake.get_head_position()[1] < y_food:
        if (y_food - this_snake.get_head_position()[1]) / 20 < (
                this_snake.get_head_position()[1] + 600 - y_food) / 20:
            y_move = 1
        else:
            y_move = -1
    else:
        x_move, y_move = this_snake.direction
    new_location = [(this_snake.get_head_position()[0] + x_move * 20 + 600) % 600,
                    (this_snake.get_head_position()[1] + y_move * 20 + 600) % 600]
    for location in other_snake.positions:
        if location[0] == new_location[0] and location[1] == new_location[1]:
            x_move, y_move = other_snake.direction[0] * -1, other_snake.direction[1] * -1
    for location in this_snake.positions:
        if location[0] == new_location[0] and location[1] == new_location[1]:
            if x_move != 0 and y_move != 0:
                flag = True
                new_location[0] -= 20 * x_move
                new_location[0] = (new_location[0] + 600) % 600
                for location1 in this_snake.positions:
                    if location1[0] == new_location[0] and location1[1] == new_location[1]:
                        y_move = 0
                if y_move != 0:
                    x_move = 0
            else:
                if x_move != 0:
                    y_move = 1
                    new_location[1] += 20
                    new_location[1] = new_location[1] % 600
                    for location in this_snake.positions:
                        if location[0] == new_location[0] and location[1] == new_location[1]:
                            y_move = -1
                else:
                    x_move = 1
                    new_location[0] += 20
                    new_location[0] = new_location[1] % 600
                    for location in this_snake.positions:
                        if location[0] == new_location[0] and location[1] == new_location[1]:
                            x_move = -1

    return (x_move, y_move)

