import grid as gd
from node import Node
from random import random


# Map Direction to 90-degrees right direction
n_right = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'}

# Map Direction to 90-degrees left direction
n_left = {'U': 'L', 'L': 'D', 'D': 'R', 'R': 'U'}

GIVEUP = 'X'


def move(node, action):
    """
    Move function takes the current node and an action and
    returns the future node using move probabilities

    :param node: Current Node
    :type node: Node
    :param action: Action to take
    :type action: str

    :return: Node we moved to
    :rtype: Node
    """
    # Grid to operate on
    grid = node.grid  # type: gd.Grid

    # MOVE
    prob = random()
    # Move occurs as expected: [0, 0.7]
    if prob <= 0.7:
        new_node = grid.move(node, action)

    # Moves 90-degrees right: (0.7, 0.8]
    elif prob <= 0.8:
        new_node = grid.move(node, n_right[action])

    # Moves 90-degrees left: (0.8, 0.9]
    elif prob <= 0.9:
        new_node = grid.move(node, n_left[action])

    # Moves double: (0.9, 1]
    else:
        new_node = grid.move(node, action)
        new_node = grid.move(new_node, action)

    return new_node


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
# Given: State
# Get States best or random action
# Use Action to get Future State
# Get State's ((Old Q-value)) and ((Future Expected Reward))
#
# Get Q-Value and Reward from Future State
#   SARSA( ((Future State)) )
#
# Return ((Future Expected Reward)) and ((New Q-Value))
def sarsa(node, alpha, gamma, depth=0):
    """
    :param node: Current State
    :type node: Node

    :param alpha: Learning Rate
    :type alpha: float
    :param gamma: Discount Rate
    :type gamma: float

    :return: newly calculated Q-Value
    :rtype: float
    """

    print('depth: ', depth)
    # Check for terminating state
    if node.is_terminating():
        return node.get_reward()

    # Get action and Check give-up
    action = node.get_action()
    if action == GIVEUP:
        return node.grid.giveup_cost

    # Old Estimate
    old_q = node.get_q_value(action)

    # Reward for taking a move
    reward = node.grid.step_cost

    # Q-Value of Future State
    future_node = move(node, action)
    future_q = sarsa(future_node, alpha, gamma, depth=depth+1)

    # Calculate new Q-Value
    new_q_value = old_q + alpha * (reward + gamma * future_q - old_q)

    # Update Node and return Updated Estimate
    node.set_q_value(new_q_value, action)
    node.set_action(action)
    return new_q_value
