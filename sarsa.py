from grid import Grid
from grid import Point
from random import random


n_right = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'}
n_left = {'U': 'L', 'L': 'D', 'D': 'R', 'R': 'U'}


# Calculates the updated Q' value
# Where q1 is s and q2 is s'
def q_function(q1, q2, reward, learning_rate, discount_factor):
    return q1 + learning_rate * (reward + discount_factor * q2 - q1)


# Decides to move or not based on epsilon
def take_random_move(epsilon):
    return random() <= epsilon


def get_action():
    return


# Move function, it is not deterministic
def move(current_node, new_node):
    grid = current_node.grid

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


# Todo: NIKO, read this explaination of how sarsa is a recursive function
#
# SARSA is a recursive function taking a state and an action and
# repeating until reaching a terminating state
#
# ===============================================================
# ======================== SARSA Formula ========================
# ===============================================================
# Q(s,a) <- Q(s,a) + alpha * [ R(s) + lambda * Q(s',a') - Q(s,a) ]
# New Q-Value = Old Q-Value + Learning-Rate *
#               ( Future Expected Reward + ( Discount-Factor * Future Q-Value ) - Old Q-Value )
#
#
# ===============================================================
# ================== SARSA Logic (pseudo code) ==================
# ===============================================================
# Given: State and Action
# Get State's ((Old Q-value)) and ((Future Expected Reward))
#
# Get Q-Value and Reward from Future State
#   Move to ((Future state)) given ((Current state and action))
#   SARSA( ((Future State)) )
#
# Return ((Future Expected Reward)) and ((New Q-Value))
#
# Input: current state, learning rate, discount rate
# Output: (future expected reward, learning rate, discount rate)
def sarsa(node, alpha, gamma):
    if node.is_terminating():
        return node.reward, 0  # reward and Q-Value

    # Old Estimate
    action = 'U'  # Todo: get best action to take
    old_q = node.get_q_value(action)

    # Expected Future Reward
    reward = node.reward

    # Q-Value of Future State
    future_node = move()  # Todo: get future node using Move()
    new_reward, future_q  = sarsa(future_node, alpha, gamma)
    new_reward = 0  # We'll also be getting a new reward value here

    new_estimate = old_q + alpha * (reward + gamma * future_q - old_q)

    # Todo: update values in current node

    return new_reward, new_estimate
