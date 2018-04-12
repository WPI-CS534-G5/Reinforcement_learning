from random import randint
from grid import Point


class Node:
    def __init__(self, row_i, col_i, state, reward):
        self.row_i = row_i
        self.col_i = col_i
        self.state = state
        self.action = randint(1, 4)
        self.reward = -0.1 + reward

        if reward > 0:
            self.p_value = 2
        else:
            self.p_value = -2

    def get_row(self):
        return self.row_i

    def get_col(self):
        return self.col_i

    def get_location(self):
        return self.row_i, self.col_i

    def get_point(self):
        return Point(self.row_i, self.col_i)

    def get_state(self):
        return self.state

    def get_action(self):
        return self.action

    def get_reward(self):
        return self.reward

    def get_p_value(self):
        return self.p_value

    def update_action(self, act):
        self.action = act

    def update_p_value(self, p):
        self.p_value = p
