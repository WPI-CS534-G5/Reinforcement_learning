from grid import Grid
from grid import Point
from random import random


n_right = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'}
n_left = {'U': 'L', 'L': 'D', 'D': 'R', 'R': 'U'}


# Calculates the updated Q' value
def q_function(q1, q2, reward, learning_rate, discount_factor):
    return q1 + learning_rate * (reward + discount_factor * q2 - q1)


# Decides to move or not based on epsilon
def take_random_move(epsilon):
    return random() <= epsilon


# Move function, it is not deterministic
def move(grid, current_node, new_node):
    new_point = new_node.get_point()  # type: Point
    current_point = current_node.get_point()  # type: Point
    direction = current_point.get_direction(new_point)

    decision = random()
    if decision <= 0.7:  # Move ocurrs as expected: [0, 0.7]
        current_point = new_point
    elif decision <= 0.8:  # Moves 90-degrees right: (0.7, 0.8]
        direction = n_right[direction]
        grid.move(current_point, direction)
    elif decision <= 0.9:  # Moves 90-degrees left: (0.8, 0.9]
        direction = n_left[direction]
        grid.move(current_point, direction)
    else:  # Moves double: (0.9, 1]
        grid.move(current_point, direction)
        grid.move(current_point, direction)

    return grid.get_node(current_point)


# something, something, update
def update():
    return
