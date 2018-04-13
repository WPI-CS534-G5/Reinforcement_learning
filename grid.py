from node import Node
from random import randrange


class Point(object):
    def __init__(self, row_i, col_i):
        self.row_i = row_i
        self.col_i = col_i

    # Mutate Point
    def move_up(self): self.row_i -= 1

    def move_down(self): self.row_i += 1

    def move_left(self): self.col_i -= 1

    def move_right(self): self.col_i += 1

    # Return new Point
    def get_move_up(self):
        p = Point(self.row_i, self.col_i)
        p.move_up()
        return p

    def get_move_down(self):
        p = Point(self.row_i, self.col_i)
        p.move_down()
        return p

    def get_move_left(self):
        p = Point(self.row_i, self.col_i)
        p.move_left()
        return p

    def get_move_right(self):
        p = Point(self.row_i, self.col_i)
        p.move_right()
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

        print(row_diff, col_diff)
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
    def up_exists(self, point): return point.get_move_up().row_i >= 0

    def down_exists(self, point): return point.get_move_down().row_i < self.num_rows

    def right_exists(self, point): return point.get_move_right().col_i < self.num_cols

    def left_exists(self, point): return point.get_move_left().col_i >= 0

    def move_exists(self, point, direction):
        actions = ['U', 'D', 'L', 'R']
        methods = [self.up_exists, self.down_exists, self.left_exists, self.right_exists]
        for action, method in zip(actions, methods):
            if direction == action:
                return method(point)
        return False

    # Check if move exists and move
    def move_up(self, point):
        if self.up_exists(point):
            return point.move_up()
        return point

    def move_down(self, point):
        if self.down_exists(point):
            return point.move_down()
        return point

    def move_left(self, point):
        if self.left_exists(point):
            return point.move_left()
        return point

    def move_right(self, point):
        if self.right_exists(point):
            return point.move_right()
        return point

    # Move point based on input direction
    def move_helper(self, point, direction):
        if direction == 'U':
            self.move_up(point)
        elif direction == 'D':
            self.move_down(point)
        elif direction == 'L':
            self.move_left(point)
        elif direction == 'R':
            self.move_left(point)

    def move(self, node, action):
        point = node.get_point()
        self.move_helper(point, action)
        return self.get_node(point)

    # Given node, get neighbors
    def get_neighbors(self, node):
        nodes = list()
        point = node.get_point()

        if self.up_exists(point):
            nodes.append(self.get_node(point.get_move_up()))
        if self.down_exists(point):
            nodes.append(self.get_node(point.get_move_down()))

        if self.right_exists(point):
            nodes.append(self.get_node(point.get_move_right()))
        if self.left_exists(point):
            nodes.append(self.get_node(point.get_move_left()))

        return nodes


# Pretty-Print on command line
def print_grid(grid, view_reward=False):
    act = {'U': '^', 'D': 'v', 'L': '<', 'R': '>', 'G': 'G', 'P': 'P'}

    for row in grid.grid:
        print('| ', end='')
        for node in row:
            if view_reward:
                p = node.get_print_reward()
            else:
                p = act[node.action]

            print(p + ' | ', end='')
        print()

