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
    # Get of new node from current node
    new_point = new_node.get_point()  # type: Point
    current_point = current_node.get_point()  # type: Point
    direction = current_point.get_direction(new_point)

    # Update Action
    current_node.update_action(direction)

    # MOVE
    prob = random()
    # Move occurs as expected: [0, 0.7]
    if prob <= 0.7:
        current_point = new_point
    # Moves 90-degrees right: (0.7, 0.8]
    elif prob <= 0.8:
        direction = n_right[direction]
        grid.move(current_point, direction)
    # Moves 90-degrees left: (0.8, 0.9]
    elif prob <= 0.9:
        direction = n_left[direction]
        grid.move(current_point, direction)
    # Moves double: (0.9, 1]
    else:
        grid.move(current_point, direction)
        grid.move(current_point, direction)

    return grid.get_node(current_point)

