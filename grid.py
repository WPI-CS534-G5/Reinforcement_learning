from node import Node
from random import randrange
from settings import UP, DOWN, LEFT, RIGHT, GIVEUP


# Helper object for Grid Class
class Point(object):
    def __init__(self, row_i, col_i):
        self.row_i = row_i
        self.col_i = col_i

    # Mutate self
    def move(self, action):
        if action == UP:
            self.row_i -= 1
            return True
        elif action == DOWN:
            self.row_i += 1
            return True
        elif action == LEFT:
            self.col_i -= 1
            return True
        elif action == RIGHT:
            self.col_i += 1
            return True

        print('Point.move([{point.row_i},{point.col_i}], {action}) got an unexpected action'.format(
            point=self, action=action))
        return False

    # Return New Point
    def get_move(self, action):
        p = Point(self.row_i, self.col_i)
        p.move(action)
        return p

    def get_direction(self, point):
        """
        Get Direction from Self to new Point
        (Points don't have to be adjacent or even exist to get answer)
        :param point: Point to get directions to
        :return: Action
        :rtype: str
        """
        row_diff = self.row_i - point.row_i
        if row_diff < 0:
            return RIGHT
        elif row_diff > 0:
            return LEFT

        col_diff = self.col_i - point.col_i
        if col_diff < 0:
            return DOWN
        elif col_diff > 0:
            return UP

        if col_diff == 0 and row_diff == 0:
            print('Point.get_direction({point.row_i},{point.col_i}) got same points'.format(point=point))
            return GIVEUP

        print("Point.get_direction() return false. Please check which universe you are in.")
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
        self.epsilon = epsilon  # exploration factor

        # Grid-World Definition
        self.num_rows = len(state_map)
        self.num_cols = len(state_map[0])
        self.grid = self.init_from_list(state_map)

        self.init_nodes()

    def init_nodes(self):
        for row in self.grid:
            for node in row:
                node.init_node()

    def init_from_list(self, matrix):
        """
        Initialize grid-world from state-map
        :param matrix: 2D List of strings representing States
        :return: 2D List of Nodes
        :rtype: list
        """
        grid = list()
        for row_i, row in enumerate(matrix):
            grid_row = list()
            for col_i, state in enumerate(row):
                grid_row.append(Node(self, row_i, col_i, state))
            grid.append(grid_row)
        return grid

    def clear_actions(self):
        for row in self.grid:
            for node in row:
                node.action = node.state
                node.actions = list()

    def get_node(self, point):
        return self.grid[point.row_i][point.col_i]

    def get_rand_node(self):
        """
        :return: Random non-terminating Node
        :rtype: Node
        """
        rand_row = randrange(0, self.num_rows)
        rand_col = randrange(0, self.num_cols)
        node = self.grid[rand_row][rand_col]

        if node.is_terminating():
            return self.get_rand_node()

        return self.grid[rand_row][rand_col]

    # Check if move exists
    def action_exists(self, point, action):
        """
        Check if this action is possible for the given point in the grid
        We return False if called from a terminating state
        :param point: Position of Node in the Grid
        :type point: Point
        :param action: Action to Check
        :type action: str
        :rtype: bool
        """
        if self.get_node(point).is_terminating():
            print('action_exists({point.row_i}, {point.col_i}, action) called from terminating state'.format(
                point=point, action=action
            ))
            return False

        new_point = point.get_move(action)

        if action == UP:
            return new_point.row_i >= 0
        elif action == DOWN:
            return new_point.row_i < self.num_rows
        elif action == RIGHT:
            return new_point.col_i < self.num_cols
        elif action == LEFT:
            return new_point.col_i >= 0
        elif action == GIVEUP:
            return True

        print('action_exists({point.row_i}, {point.col_i}, {action}) got unexpected action'.format(
            point=point, action=action))
        return False

    def move(self, node, action):
        """
        Make a move given a node and and action to take.
        IF MOVE DOESN'T EXIST, WE RETURN THE SAME NODE. IT IS NOT THIS
        FUNCTION'S JOB TO CHECK FOR VALIDITY. SAVE IT FOR THE LOGS

        :param node: Node in the Grid
        :type node: Node
        :param action: Action to Take
        :type action: str

        :return: New Node base off old Node and Action taken
        :rtype: Node
        """
        point = node.get_point()
        if self.action_exists(point, action):
            point.move(action)
            return self.get_node(point)
        return node
