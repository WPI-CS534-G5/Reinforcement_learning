import grid as gd
from random import random
from random import randrange


DEBUG = True

# Todo: move these lists into their own module
# ####### List of possible actions for each state ####### #
# U: Up
# D: Down
# L: Left
# R: Right
# S: Stay  --> check for this but should never happen
# X: Give-up
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
GIVEUP = 'G'

# ####### List of Possible States ####### #
# G: Goal
# P: Pit
# O: Regular
PIT = 'P'
GOAL = 'G'
NORM = 'O'


class Node(object):
    def __init__(self, grid, row_i, col_i, state):
        """
        :param grid: a state representation of a grid world
        :type grid: gd.Grid

        :param row_i: row position in grid world
        :type row_i: int
        :param col_i: column position in grid world
        :type col_i: int

        :param state: description of type of state (Goal, Pit, Regular)
        :type state: str
        """

        # Grid and self.Position
        self.grid = grid
        self.row_i = row_i
        self.col_i = col_i

        self.action = None      # The latest action taken
        self.actions = list()   # A list of the actions taken
        self.q_values = dict()  # One for each action
        self.state = state      # (Goal, Pit, Normal)

    # Todo: come up with clever initialization (manhattan distance from goal/pit?)
    def init_q_values(self):
        return

    # Initialize action, actions, and Q-Values
    def init_node(self):
        if self.is_terminating():
            return

        self.action = None  # No actions taken yet

        # Set Possible Actions and their Q-Values
        all_actions = [LEFT, RIGHT, UP, DOWN]
        for action in all_actions:
            if self.grid.action_exists(self.get_point(), action):
                self.q_values[action] = 0

    def get_reward(self):
        """
        Gets the Reward(a.k.a step-cost) based off the state type
        :return: reward
        :rtype: float
        """
        if self.state == GOAL:
            return self.grid.goal_reward
        elif self.state == PIT:
            return self.grid.pit_reward
        elif self.action == GIVEUP:
            return self.grid.giveup_cost
        else:
            return self.grid.step_cost

    def get_point(self):
        return gd.Point(self.row_i, self.col_i)

    def set_q_value(self, q_value, action):
        self.q_values[action] = q_value

    def get_q_value(self, action=None, random_value=False):
        """
        Gets the Q-Value of the action for this state/node
        If action is not provided, we return the best Q-Value using get_best_action()
        If random_value is set, we return a random Q-Value (why? I don't know son)
        :param action: action to look for
        :param random_value: whether or not to return a random Q-Value
        :return: Q-Value based on action
        :rtype: float
        """
        if self.is_terminating():
            return self.get_reward()

        if random_value:
            actions = list(self.q_values.keys())
            return self.q_values[actions[randrange(len(actions))]]

        if action is None:
            action = self.get_best_action()
            return self.q_values[action]

        return self.q_values[action]

    def set_action(self, action):
        self.action = action
        self.actions.append(action)
        return

    def get_latest_action(self):
        return self.actions[-1]

    def get_best_action(self, printing=False):
        """
        Basically ARGMAX(Q-Value), but also return a random action if multiple are the same
        Unless this function is being used for printing out values,
        we should not be calling this function from a terminating node
        :param printing: whether or not this is being used to print
        :return: best action based on Q-Values
        :rtype: str
        """

        #  ####### Check for terminating state ####### #
        if self.is_terminating():
            if printing:
                print('Running get_action() from terminating state. THIS SHOULDNT BE HAPPENING')
            return self.state

        # ####### Check for random move ####### #
        if random() <= self.grid.epsilon:
            actions = list(self.q_values.keys())
            r_i = randrange(0, len(actions))
            return actions[r_i]

        # ####### Find Best Moves ####### #
        # Get list of q-values
        actions = list(self.q_values.items())
        actions.sort()

        best = actions.pop(0)
        best_action = best[0]
        best_value = best[1]

        # Find best move(s)
        best_actions = [best_action]
        for action, value in actions:
            if value == best_value:
                best_actions.append(action)

        # If >1 best moves, return random action
        if len(best_actions) == 1:
            best_action = best_actions[0]
        else:
            r_i = randrange(len(best_actions))
            best_action = best_actions[r_i]

        return best_action

    # Return True if this node is a terminating state
    def is_terminating(self):
        return self.state == GOAL or self.state == PIT


# ####### Start of functions non-essential to sarsa ####### #
# Debug, assignment output, etc


# Return printable string of reward value
def get_print_reward(node):
    if node.is_terminating():
        return '{:^5}'.format(node.state)

    reward = node.get_q_value(node.get_best_action(printing=True))
    if reward < 0:
        return '{0:2.2f}'.format(reward)
    else:
        return '+{0:2.2f}'.format(reward)

def get_debug_reward(node):
    if node.is_terminating():
        return '{:^5}'.format(node.state)

    reward = node.get_q_value(node.action)
    if reward < 0:
        return '{0:2.2f}'.format(reward)
    else:
        return '+{0:2.2f}'.format(reward)
