import grid as gd
from random import random
from random import randrange


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

        # Grid and Position on it
        self.grid = grid
        self.row_i = row_i
        self.col_i = col_i
        self.point = gd.Point(row_i, col_i)

        # Recommended action based on Q-Values
        self.action = ['L', 'R', 'U', 'D', 'X'][randrange(5)]

        # What kind of state is this? (Goal, Pit, Regular)
        self.state = state

        # (U)p, (D)own, (L)eft, (R)ight, (X)Give-up
        self.q_values = dict()

        self.init_node()
        self.init_q_values()

    def init_node(self):
        # If terminating state, there are no moves
        if self.is_terminating():
            self.action = self.state

        # Get Current State and All Actions
        point = self.get_point()
        actions = ['L', 'R', 'U', 'D']

        # Add Potential Actions from Current State
        for action in actions:
            if self.grid.move_exists(point, action):
                self.q_values[action] = -2

        # Add Give-Up as Potential Move
        self.q_values['X'] = self.grid.giveup_cost

    def get_point(self):
        return self.point

    def get_reward(self):
        if self.state == 'G':
            return self.grid.goal_reward
        elif self.state == 'P':
            return self.grid.pit_reward
        elif self.action == 'X':
            return self.grid.giveup_cost
        else:
            return self.grid.step_cost

    # Todo: come up with clever initialization (manhattan distance from goal/pit?)
    def init_q_values(self):
        return

    def set_q_value(self, q_value, action):
        self.q_values[action] = q_value

    def get_q_value(self, action):
        return self.q_values[action]

    def set_action(self, action):
        self.action = action
        return

    def get_action(self, printing=False):

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

        # Update node's action
        self.action = best_action
        return best_action

    # Return True if this node is a terminating state
    def is_terminating(self):
        return self.state == 'G' or self.state == 'P'

    # Return printable string of reward value
    def get_print_reward(self):
        if self.is_terminating():
            return '{:^5}'.format(self.state)

        reward = self.get_q_value(self.action)
        if reward < 0:
            return '{0:2.2f}'.format(reward)
        else:
            return '+{0:2.2f}'.format(reward)
