from node import Node
from grid import Grid


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

# ####### Map Action Representation to Print Character ####### #
act = {UP: '^', DOWN: 'v', LEFT: '<', RIGHT: '>', GIVEUP: 'G', GOAL: '#', PIT: 'P', NORM: '*'}


# Return printable string of reward value
def get_print_reward(node, best=True):
    """
    :param node: Node to get reward from
    :type node: Node
    :return: printable reward string
    :rtype: str
    """
    if node.is_terminating():
        return '{:^5}'.format(node.state)

    if best:
        reward = node.get_q_value(node.get_best_action())
    else:
        reward = node.get_q_value(node.action)

    if reward < 0:
        return '{0:2.2f}'.format(reward)
    else:
        return '+{0:2.2f}'.format(reward)


def get_print_action(node, best=True):
    if node.is_terminating():
        return act[node.state]

    if best:
        return act[node.get_best_action()]

    return act[node.action]


# Pretty-Print on command line
def print_grid(grid, best_path=True, view_reward=False):
    """
    Pretty print of Grid's state actions
    :param grid: Grid to print
    :type grid: Grid

    :param best_path: print latest path or best path?
    :type best_path: bool
    :param view_reward: print reward grid or action grid?
    :type view_reward: bool
    """

    if not view_reward:
        print('|---+---+---+---+---+---+---|')
        for row in grid.grid:
            p = '| '
            for node in row:
                p += get_print_action(node, best=best_path) + ' | '
            print(p)
            print('|---+---+---+---+---+---+---|')
    else:
        print('|-------+-------+-------+-------+-------+-------+-------|')
        for row in grid.grid:
            p = '| '
            for node in row:
                p += get_print_reward(node, best=best_path) + ' | '
            print(p)
            print('|-------+-------+-------+-------+-------+-------+-------|')