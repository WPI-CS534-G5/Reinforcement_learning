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

        # Recommended action based on Q-Values
        self.action = ['U', 'D', 'L', 'R'][randrange(4)]

        # What kind of state is this? (Goal, Pit, Regular)
        self.state = state

        # Store Q-Value for every action
        # (U)p, (D)own, (L)eft, (R)ight, (X)Give-up
        self.q_values = dict()

        self.init_node()
        self.init_q_values()

    def init_node(self):
        # {'U': 2.0, 'D': 2.0, 'L': 2.0, 'R': 2.0, 'X': grid.giveup_cost}
        if self.is_terminating():
            self.action = self.state

        point = self.get_point()
        actions = ['L', 'R', 'U', 'D']
        for action in actions:
            if self.grid.move_exists(point, action):
                self.q_values[action] = 2
        self.q_values['X'] = self.grid.giveup_cost

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

    # Todo: fix this shit-show of a function
    def get_action(self):
        # Check for terminating state
        if self.is_terminating():  # WE SHOULD NEVER HIT THIS!!
            print('Running get_action() from terminating state. THIS SHOULDNT BE HAPPENING')
            return self.state

        # Check for random move
        if random() <= self.grid.epsilon:
            actions = list(self.q_values.keys())
            r_i = randrange(0, len(actions))
            return actions[r_i]

        # Get list of q-values
        actions = list(self.q_values.items())
        actions.sort()

        best = actions.pop(0)
        best_action = best[0]
        best_value = best[1]

        # Find best move(s)
        equal = [best_action]
        for action, value in actions:
            if value == best_value:
                equal.append(action)

        # If >1 best moves, return random action
        if len(equal) == 1:
            best_action = equal[0][0]
        else:
            r_i = randrange(0, len(equal))
            best_action = equal[r_i][0]

        # Update node's action
        self.action = best_action
        return best_action

    def get_point(self):
        return gd.Point(self.row_i, self.col_i)

    def set_point(self, point):
        self.row_i = point.row_i
        self.col_i = point.col_i

    def get_reward(self):
        if self.state == 'G':
            return self.grid.goal_reward
        elif self.state == 'P':
            return self.grid.pit_reward
        else:
            return self.grid.step_cost

    def is_terminating(self):
        return self.state == 'G' or self.state == 'P'

    def get_print_reward(self):
        if self.is_terminating():
            return ':^5'.format(self.state)

        reward = self.get_q_value(self.action)
        return '{:2.2f}'.format(reward)
