import grid as gd
from node import Node
from random import random
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
        if new_node.is_terminating():
            return new_node
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


def update_node(node, q_value, action):
    node.set_q_value(q_value, action)
    node.set_action(action)


# New Q-Value = Old Q-Value + Learning-Rate *
#               ( Step-Discount + ( Discount-Factor * Future Q-Value ) - Old Q-Value )
def sarsa_eduardo(node, alpha, gamma):

    actions = list()
    actual_actions = list()
    future_expected_rewards = list()
    while not node.is_terminating():

        # Get Action and Check for Give-up
        action = get_action(node)
        actions.append(action)
        if action == GIVEUP:
            update_node(node, node.grid.giveup_cost, action)
            break

        q = node.get_q_value(action)
        reward = node.get_reward()
        node_prime, q_prime = get_prime(node, action)
        new_q = q + (alpha * (reward + (gamma * q_prime) - q))

        #
        # DEBUG STATEMENTS
        future_expected_rewards.append(new_q)
        point_start = node.get_point()
        point_end = node_prime.get_point()
        a = point_start.get_direction(point_end)
        actual_actions.append(a)
        #

        update_node(node, new_q, action)
        node = node_prime

    print('Intended Actions: ', actions)
    print('Actual Actions:   ', actual_actions)
    return future_expected_rewards


#
#
#
#
#
#
#
#
#
#
#
#
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
# Given: State
# Get States best or random action
# Use Action to get Future State
# Get State's ((Old Q-value)) and ((Future Expected Reward))
#
# Get Q-Value and Reward from Future State
#   SARSA( ((Future State)) )
#
# Return ((Future Expected Reward)) and ((New Q-Value))
def sarsa(node, alpha, gamma):
    """
    WARNING: Stack-Overflow with Small Epsilon Values
    :param node: Current State
    :type node: Node

    :param alpha: Learning Rate
    :type alpha: float
    :param gamma: Discount Rate
    :type gamma: float

    :return: newly calculated Q-Value
    :rtype: float
    """
    # Check for terminating state
    if node.is_terminating():
        return node.get_reward()

    # Get action and Check give-up
    action = get_action(node)
    if action == GIVEUP:
        reward = node.grid.giveup_cost
        update_node(node, reward, GIVEUP)
        return reward

    # ####### Calculate Function ####### #
    q = node.get_q_value(action)                            # Old Estimate
    reward = node.get_reward()                              # Reward for taking a move
    node_prime, q_prime = get_prime(node, action)           # Q-Value of Future State
    new_q = q + (alpha * (reward + (gamma * q_prime) - q))  # Calculate new Q-Value

    # Update Node and return Updated Estimate
    update_node(node, new_q, action)

    return new_q


def sarsa_iterative(starting_node, alpha, gamma):
    """
    :param starting_node: Starting node
    :type starting_node: Node

    :param alpha: Learning Rate
    :param gamma: Discount Rate

    :return: idk man
    """

    node = starting_node
    nodes = list()
    actions = list()

    # Get Path taken by agent
    while not node.is_terminating():

        # Get action and Check give-up
        action = node.get_best_action()
        actions.append(action)
        if action == GIVEUP:
            node.action = GIVEUP
            nodes.append(node)
            break

        # Get new node using action
        node = move(node, action)
        nodes.append(node)

    # Last Q-Value
    node = nodes.pop()
    new_q = node.get_reward()

    # Update Q-Values with resulting list of nodes
    while nodes:
        node = nodes.pop()
        action = actions.pop()
        reward = node.get_reward()
        old_q = node.get_q_value(action)

        new_q_value = old_q + (alpha * (reward + (gamma * new_q) - old_q))
        node.set_q_value(new_q_value, action)

    return
