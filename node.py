import grid as gd
from random import randrange


class Node:
    def __init__(self, row_i, col_i, state, reward):
        self.row_i = row_i
        self.col_i = col_i
        self.state = state
        self.action = ['U', 'D', 'L', 'R'][randrange(4)]
        self.reward = reward

        if reward > 0:
            self.q_value = 2
        else:
            self.q_value = -2

        self.directions = {'U': 0, 'D': 1, 'L': 2, 'R': 3}

    def get_row(self):
        return self.row_i

    def get_col(self):
        return self.col_i

    def get_location(self):
        return self.row_i, self.col_i

    def get_point(self):
        return gd.Point(self.row_i, self.col_i)

    def get_state(self):
        return self.state

    def get_action(self):
        return self.action

    def get_reward(self):
        return self.reward

    def get_q_value(self):
        return self.q_value

    def update_action(self, act):
        self.action = act

    def update_q_value(self, p):
        self.q_value = p
