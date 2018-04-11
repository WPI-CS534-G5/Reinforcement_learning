from random import randint


class Node:
    def __init__(self, x, y, state, reward):
        self.x = x
        self.y = y
        self.state = state
        self.action = randint(1, 4)
        self.reward = -0.1 + reward

        if reward > 0:
            self.p_value = 2
        else:
            self.p_value = -2

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

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
