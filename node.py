import grid as gd
from random import randrange


class Node:
    def __init__(self, row_i, col_i, state, grid):

        # Grid and Position on it
        self.grid = grid
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
        self.q_values = {'U': 2, 'D': 2,
                         'L': 2, 'R': 2}

    def update_action(self):
        self.action = self.get_action()
        return

    def get_action(self):
        actions = list(self.q_values.items())
        actions.sort()

        best_action = actions.pop(0)
        equal = [best_action]
        for action in actions:
            if action == best_action:
                equal.append(action)

        if len(actions) == 1:
            return actions[0]
        else:
            r_i = randrange(0, len(actions))
            return actions[r_i]

    def update_reward(self, new_reward):
        if new_reward > self.reward:
            self.reward = new_reward

    def get_q_value(self, action):
        return self.q_values[action]

    def set_q_value(self, action):
        return self.q_values[action]

    def get_point(self):
        return gd.Point(self.row_i, self.col_i)

    def is_terminating(self):
        return self.state == 'G' or self.state == 'P'
