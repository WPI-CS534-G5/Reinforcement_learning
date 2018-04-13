import sarsa
import node
import grid  as gd
from sys import argv
from random import randrange

# goal_reward = argv[1]
# pit_reward = argv[2]
# move_cost = argv[3]
# giveup_cost = argv[4]
# trials = argv[5]
# epsilon = argv[6]
goal_reward = 5
pit_reward = -2
move_cost = -0.1
giveup_cost = -3
num_iterations = 10000
epsilon = 0.1

p = 'P'
g = 'G'
num_rows = 6
num_cols = 7
state_map = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, p, p, 0, 0, 0],
             [0, p, g, 0, 0, p, 0],
             [0, 0, p, p, p, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]

# The learning rate determines to what extent newly acquired information overrides old information.
# A factor of 0 will make the agent not learn anything, while a factor of 1 would make
#  the agent consider only the most recent information.
alpha = 0.5  # Learning Rate

# The discount factor determines the importance of future rewards. A factor
# of 0 makes the agent "opportunistic" by only considering current rewards,
# while a factor approaching 1 will make it strive for a long-term high reward.
# If the discount factor meets or exceeds 1, the Q values may diverge.
gamma = 0.5  # Discount Factor


# Initialize the map
grid = gd.Grid(state_map, goal_reward, pit_reward)


for iteration in range(num_iterations):

    # Get a random position
    current_point = grid.get_rand_position()  # type: gd.Point
    current_node = grid.get_node(current_point)  # type: node.Node

    # Todo: we probably don't need this while loop
    # While your current position is not on a terminating state
    while not current_node.is_terminating():

        # Get all the neighbors of the current position
        neighbors = grid.get_neighbors(current_node)

        # Probability of taking random move
        if sarsa.take_random_move(epsilon):
            new_node = neighbors[randrange(len(neighbors))]
            current_node = sarsa.move(grid, current_node, new_node)
            continue

        # Find neighbor with best q-value
        best_node = None
        max_q_value = None
        for new_node in neighbors:
            current_q_value = current_node.get_q_value()
            future_q_value = new_node.get_q_value()
            future_reward = new_node.get_reward()
            new_q_value = sarsa.q_function(current_q_value, future_q_value, future_reward,
                                           alpha, gamma)

            if max_q_value is None or new_q_value > max_q_value:
                best_q_value = new_q_value
                best_node = new_node

        current_node = sarsa.move(grid, current_node, best_node)

# See the resulting board
gd.print_grid(grid)


