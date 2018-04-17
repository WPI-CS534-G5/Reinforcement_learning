import grid as gd
from node import Node
from random import random
from settings import SARSA_DEBUG as DEBUG
from settings import UP, DOWN, LEFT, RIGHT, GIVEUP

# Map Direction to 90-degrees right direction
n_right = {UP: 'R', RIGHT: 'D', DOWN: 'L', LEFT: 'U'}

# Map Direction to 90-degrees left direction
n_left = {UP: 'L', LEFT: 'D', DOWN: 'R', RIGHT: 'U'}


def move(node, action):
    """
    Move function takes the current node and an action and
    returns the future node using move probabilities

    THIS FUNCTION DOES NOT MUTATE THE CURRENT NODE BUT
    INSTEAD RETURNS A NEW NODE

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
        if not new_node.is_terminating():
            new_node = grid.move(new_node, action)

    return new_node


def get_action(node):
    if random() <= node.grid.epsilon:
        return node.get_random_action()
    return node.get_best_action(random_best=True)


def get_prime(node, action):
    node_prime = move(node, action)  # move(action) to get s'
    q_prime = node_prime.get_best_q_value()  # ARGMAX[Q-Values] to get a'
    return node_prime, q_prime


# New Q-Value = Old Q-Value + Learning-Rate *
#               ( Step-Discount + ( Discount-Factor * Future Q-Value ) - Old Q-Value )
def sarsa_eduardo(node, alpha, gamma):

    future_expected_rewards = list()
    while not node.is_terminating():

        # Get Action and Check for Give-up
        action = get_action(node)
        node.set_action(action)
        if action == GIVEUP:
            reward = node.get_reward()
            node.set_q_value(reward, action)
            future_expected_rewards.append(reward)
            break

        # ####### Q-Function ####### #
        q = node.get_q_value(action)                            # Old Estimate
        reward = node.get_reward()                              # Reward for taking move
        future_expected_rewards.append(reward)
        node_prime, q_prime = get_prime(node, action)           # Q-Value of Future State
        new_q = q + (alpha * (reward + (gamma * q_prime) - q))  # Calculate new Q-Value

        # ####### Update Node and Set Node ####### #
        node.set_q_value(new_q, action)
        node = node_prime

    future_expected_rewards.append(node.get_reward())
    return sum(future_expected_rewards)
