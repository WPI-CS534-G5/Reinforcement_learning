from node import Node
from random import randrange


class Point(object):
    '''Point Class'''
    def __init__(self, row_i, col_i):
        self.row_i = row_i
        self.col_i = col_i

    # Mutate Point
    def move_up(self):
        self.row_i -= 1

    def move_down(self):
        self.row_i += 1

    def move_left(self):
        self.col_i -= 1

    def move_right(self):
        self.col_i += 1

    # Return new Point
    def get_move_up(self):
        return Point(self.row_i - 1, self.col_i)

    def get_move_down(self):
        return Point(self.row_i + 1, self.col_i)

    def get_move_left(self):
        return Point(self.row_i, self.col_i - 1)

    def get_move_right(self):
        return Point(self.row_i, self.col_i + 1)

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


class Grid(object):
    """Grid
    Creates a matrix of nodes. nothing else
    """
    def __init__(self, state_map, goal_reward, pit_reward):
        self.pit_reward = pit_reward
        self.goal_reward = goal_reward

        self.grid = self.init_from_map(state_map)
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])

    # Initialize grid-world from state_map
    def init_from_map(self, matrix):
        m = list()
        for row_i, row in enumerate(matrix):
            new_row = list()

            for col_i, state in enumerate(row):
                reward = 0
                if state == 'P':
                    reward = self.pit_reward
                elif state == 'G':
                    reward = self.goal_reward

                new_row.append(Node(row_i, col_i, state, reward))
            m.append(new_row)
        return m

    def get_node(self, point):
        return self.grid[point.row_i][point.col_i]

    # Returns random coordinate that is not pit or goal state
    def get_rand_position(self):
        rand_row = randrange(0, self.num_rows)
        rand_col = randrange(0, self.num_cols)
        state = self.grid[rand_row][rand_col].get_state()

        if (state == 'P') or (state == 'G'):
            return self.get_rand_position()

        return Point(rand_row, rand_col)

    # FOR_DEBUGGING: Takes in a coordinate and sets a flag on the map
    def set_flag(self, row, col, flag_val): self.grid[row][col] = flag_val

    # Check if move exists
    def up_exists(self, point):
        up = point.get_move_up()
        return up.row_i >= 0

    def down_exists(self, point):
        down = point.get_move_down()
        return down.row_i < self.num_rows

    def right_exists(self, point):
        right = point.get_move_right()
        return right.col_i < self.num_cols

    def left_exists(self, point):
        left = point.get_move_left()
        return left.col_i >= 0

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
    def move(self, point, direction):
        if direction == 'U':
            self.move_up(point)
        elif direction == 'D':
            self.move_down(point)
        elif direction == 'L':
            self.move_left(point)
        elif direction == 'R':
            self.move_left(point)

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
    p = {'U': '^', 'D': 'v', 'L': '<', 'R': '>', 0: '0'}

    for row in grid.grid:
        print('| ', end='')

        for node in row:
            if node.state in ['P', 'G']:
                print(node.state, end='')
            else:
                print(p[node.action], end='')
            print(' | ', end='')
        print()
