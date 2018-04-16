import grid as gd
from random import randrange
from settings import UP, DOWN, LEFT, RIGHT, GIVEUP, GOAL, PIT, NORM


DEBUG = True


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

    def init_node(self):     # Initialize action, actions, and Q-Values
        if self.is_terminating():
            return

        self.action = self.state  # No actions taken yet

        # Set Possible Actions and their Q-Values
        all_actions = [LEFT, RIGHT, UP, DOWN, GIVEUP]
        for action in all_actions:
            if self.grid.action_exists(self.get_point(), action):
                self.q_values[action] = 0
        self.q_values[GIVEUP] = self.grid.giveup_cost

    def get_point(self):
        return gd.Point(self.row_i, self.col_i)

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

    # ####### ######## ####### ######### ######## ####### #
    # ####### ######## Q-VALUE FUNCTIONS ######## ####### #
    # ####### ######## ####### ######### ######## ####### #
    # These functions are used to acquire q-values in specific ways
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
        if action == self.state:
            return 0
        if random_value or not action:
            actions = list(self.q_values.keys())
            return self.q_values[actions[randrange(len(actions))]]

        return self.q_values[action]

    def get_best_q_value(self):
        if self.is_terminating():
            return self.get_reward()

        action = self.get_best_action()
        return self.get_q_value(action)

    def set_q_value(self, q_value, action):
        self.q_values[action] = q_value

    # ####### ######## ###### ######### ######## ####### #
    # ####### ######## ACTION FUNCTIONS ######## ####### #
    # ####### ######## ###### ######### ######## ####### #
    # These functions are used to acquire actions in specific ways
    def get_latest_action(self):
        return self.actions[-1]

    def get_random_action(self):
        actions = list(self.q_values.keys())
        r_i = randrange(len(actions))
        return actions[r_i]

    def get_best_action(self, random_best=False):
        """
        Returns only one best action
        :param random_best: whether or not to get a random action from best list
        :return: action requested from list of best actions
        """
        actions = self.get_best_actions()
        if len(actions) == 1 or not random_best:
            return actions[0]
        return actions[randrange(len(actions))]

    def get_best_actions(self, printing=False):
        """
        Basically ARGMAX(Q-Value), but also return a random action if multiple are the same
        Unless this function is being used for printing out values,
        we should not be calling this function from a terminating node
        :param printing: whether or not this is being used to print
        :return: best action based on Q-Values
        :rtype: str
        """

        #  Check for terminating state
        if self.is_terminating():
            if printing:
                print('Running get_action() from terminating state. THIS SHOULDNT BE HAPPENING')
            return self.state

        # Get possible moves
        a = list(self.q_values.items())
        actions = list()
        for action, value in a:
            actions.append(tuple([value, action]))

        # Find best move(s)
        actions.sort(reverse=True)
        best = actions.pop(0)
        if best[0] < self.grid.giveup_cost:
            return GIVEUP

        same_actions = [best[1]]
        for action_tup in actions:  # [ (value, key) ] <--> [ (q-value, action) ]
            if action_tup[0] == best[0]:
                same_actions.append(action_tup[1])

        # print(same_actions)
        return same_actions

    def set_action(self, action):
        self.action = action
        self.actions.append(action)
        return

    def is_terminating(self):
        return self.state == GOAL or self.state == PIT
