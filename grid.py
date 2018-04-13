from node import Node
from random import randrange


# Helper object for Grid Class
class Point(object):
    def __init__(self, row_i, col_i):
        self.row_i = row_i
        self.col_i = col_i

    def move(self, action):
        if action == 'U':
            self.row_i -= 1
            return True
        elif action == 'D':
            self.row_i += 1
            return True
        elif action == 'L':
            self.col_i -= 1
            return True
        elif action == 'R':
            self.col_i += 1
            return True

        print('point.move({move}) returned False'.format(move=action))
        return False

    def get_move(self, action):
        p = Point(self.row_i, self.col_i)
        p.move(action)
        return p

    # Get direction from self to new point
    def get_direction(self, point):
        row_diff = self.row_i - point.row_i
        if row_diff < 0:
            return 'R'
        elif row_diff > 0:
            return 'L'

        col_diff = self.col_i - point.col_i
        if col_diff < 0:
            return 'D'
        elif col_diff > 0:
            return 'U'

        print('get_direction({point.row_i},{point.col_i}) returning False'.format(point=point))
        return False


# Store Grid-World
class Grid(object):
    """Grid
    Creates a matrix of nodes. nothing else
    """
    def __init__(self, state_map, goal_reward, pit_reward, step_cost, giveup_cost, epsilon):
        # Grid-World Parameters
        self.pit_reward = pit_reward
        self.goal_reward = goal_reward
        self.step_cost = step_cost
        self.giveup_cost = giveup_cost
        self.epsilon = epsilon

        # Grid-World Definition
        self.num_rows = len(state_map)
        self.num_cols = len(state_map[0])
        self.grid = self.init_from_map(state_map)

    # Initialize grid-world from state_map
    def init_from_map(self, matrix):
        m = list()
        for row_i, row in enumerate(matrix):
            new_row = list()
            for col_i, state in enumerate(row):
                new_row.append(Node(self, row_i, col_i, state))
            m.append(new_row)
        return m

    def get_node(self, point):
        return self.grid[point.row_i][point.col_i]

    # Returns random coordinate that is not pit or goal state
    def get_rand_node(self):
        rand_row = randrange(0, self.num_rows)
        rand_col = randrange(0, self.num_cols)
        state = self.grid[rand_row][rand_col].state

        if (state == 'P') or (state == 'G'):
            return self.get_rand_node()

        return self.grid[rand_row][rand_col]

    # Check if move exists
    def move_exists(self, point, action):
        new_point = point.get_move(action)

        if action == 'U':
            return new_point.row_i >= 0
        elif action == 'D':
            return new_point.row_i < self.num_rows
        elif action == 'R':
            return new_point.col_i < self.num_cols
        elif action == 'L':
            return new_point.col_i >= 0

        print('move_exists({0}, {1}) returned False'.format(point, action))
        return False

    def move(self, node, action):
        point = node.get_point()
        if self.move_exists(point, action):
            point.move(action)

        return self.get_node(point)


# Pretty-Print on command line
def print_grid(grid, view_reward=False):
    act = {'U': '^', 'D': 'v', 'L': '<', 'R': '>', 'G': '#', 'P': 'P', 'X': 'G'}

    if not view_reward:
        print('|---+---+---+---+---+---+---|')
        for row in grid.grid:
            p = '| '
            for node in row:
                p += act[node.get_action()] + ' | '
            print(p)
            print('|---+---+---+---+---+---+---|')
    else:
        print('|-------+-------+-------+-------+-------+-------+-------|')
        for row in grid.grid:
            p = '| '
            for node in row:
                p += node.get_print_reward() + ' | '
            print(p)
            print('|-------+-------+-------+-------+-------+-------+-------|')


