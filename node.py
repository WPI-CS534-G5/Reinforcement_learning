import grid as gd
from random import randrange


class Node:
    def __init__(self, row_i, col_i, state):

        # Positino in grid
        self.row_i = row_i
        self.col_i = col_i

        # What kind of state is this? (Goal, Pit, Regular)
        self.state = state

        # Recommended action based on Q-Values
        self.action = ['U', 'D', 'L', 'R'][randrange(4)]

        # Expected Future Reward
        self.reward = 0

        # Store Q-Value for every action
        # Use this dict to access individual Q-Values
        self.q_values = {'U': 0, 'D': 0,
                         'L': 0, 'R': 0}

    # Todo: Set action based on best Q-Value
    def update_action(self, act):
        return

    # Todo: return best action based: Max(Q-Value)
    def get_action(self):
        return self.action

    # Todo: update reward if it's better
    def update_reward(self, new_reward):
        return

    def get_q_value(self, action):
        return self.q_values[action]

    def set_q_value(self, action):
        return self.q_values[action]

    def get_point(self):
        return gd.Point(self.row_i, self.col_i)

    def is_terminating(self):
        return self.state == 'G' or self.state == 'P'
