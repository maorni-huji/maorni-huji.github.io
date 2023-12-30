import classes
from classes import RIGHT, LEFT, UP, DOWN  # directions
import random

"""
Your very own snake!
Receives a copy of the food, which grants you a point and makes you one unit longer.
Receives a copy of the superfood, which grants you 5 points, and makes you 5 units longer.
Receives your own snake, and receives to opponents snake.
Returns the direction the snake will be facing.
"""
N = (0,1)
E = (1,0)
S = (0,-1)
W = (-1,0)
NE = (1,1)
SE = (1,-1)
SW = (-1,-1)
NW = (-1,1)
ALLOWED_DIRECTIONS = [N, S, W, E, NE, SE, SW, NW]
SUPERFOOD_TIMER = 50
GRID_SIZE = 600
import math

def duplicate_positions(positions):
    #duplicate positions because we can cross through walls
    new_positions = []
    for pos in positions:
        new_positions.append(pos)
        for dir in ALLOWED_DIRECTIONS:
            new_positions.append((pos[0] + dir[0]*GRID_SIZE, pos[1] + dir[1]*GRID_SIZE))
            
    return new_positions

def get_closest_virtual_point(p1, p2):
    p2_pos = duplicate_positions([p2])
    p2_distance = []
    for pos in p2_pos:
        p2_distance.append(max(abs(p1[0] - pos[0]),abs(p1[1] - pos[1])))
    return p2_pos[p2_distance.index(min(p2_distance))]

def calculate_distance(point1, point2):
    p2_pos = get_closest_virtual_point(point1, point2)
    return max(abs(point1[0] - p2_pos[0])/20,abs(point1[1] - p2_pos[1])/20)

def calc_distance_to_any_snake(snake, other_snake):
    positions = other_snake.positions + snake.positions
    positions = duplicate_positions(positions)
    distances = {}
    for direction in ALLOWED_DIRECTIONS:
        head_pos = snake.get_head_position()
        head_pos = (head_pos[0] + direction[0]*20, head_pos[1] + direction[1]*20)
        distance = 0
        while head_pos not in positions:
            head_pos = (head_pos[0] + direction[0]*20, head_pos[1] + direction[1]*20)
            distance += 20
            if distance >= 600:
                break
        
        distances[direction] = distance
    
    return distances

def goto(snake, position):
    head_pos = snake.get_head_position()
    position = get_closest_virtual_point(head_pos, position)
    if head_pos[0] < position[0] and head_pos[1] < position[1]:
        return NE
    elif head_pos[0] < position[0] and head_pos[1] > position[1]:
        return SE
    elif head_pos[0] > position[0] and head_pos[1] < position[1]:
        return NW
    elif head_pos[0] > position[0] and head_pos[1] > position[1]:
        return SW
    elif head_pos[0] < position[0] and head_pos[1] == position[1]:
        return E
    elif head_pos[0] > position[0] and head_pos[1] == position[1]:
        return W
    elif head_pos[0] == position[0] and head_pos[1] < position[1]:
        return N
    elif head_pos[0] == position[0] and head_pos[1] > position[1]:
        return S
    else:
        return snake.direction


def should_suicide(this_snake,other_snake):
    if this_snake.get_score() > other_snake.get_score() + 20:
        return True
    return False

def think(food : classes.Food, superfood: classes.Superfood, this_snake : classes.Snake, other_snake: classes.Snake):
    # Calculate distance
    global SUPERFOOD_TIMER
    superfood_distance = calculate_distance(this_snake.get_head_position(), superfood.position)
    snake_distance = calc_distance_to_any_snake(this_snake, other_snake)
    allowed_directions_for_this_turn = [direction for direction in ALLOWED_DIRECTIONS if snake_distance[direction] >= 2]
    
    #If I can get to superfood in time, go for it
    if should_suicide(this_snake,other_snake):
        sec_pos = this_snake.positions[2]
        direction = goto(this_snake, sec_pos)
        if direction == (-this_snake.direction[0], -this_snake.direction[1]):
            if direction == E or direction == S:
                direction = SE
            if direction == W or direction == N:
                direction = NW
            if direction == SE or direction == NE:
                direction = E
            if direction == SW or direction == NW:
                direction = W
                
        return direction
    
    if superfood.is_hidden:
        SUPERFOOD_TIMER = 50
    
    if not superfood.is_hidden:
        if superfood_distance < SUPERFOOD_TIMER:
            direction = goto(this_snake, superfood.position)
            
        SUPERFOOD_TIMER -= 1
    
    if superfood.is_hidden or superfood_distance > SUPERFOOD_TIMER:
        direction = goto(this_snake, food.position)
    if direction in allowed_directions_for_this_turn:
        return direction
    else:
        return random.choice(allowed_directions_for_this_turn)

#test get_closest_virtual_point
