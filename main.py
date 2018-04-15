import grid as gd
from node import Node
from sarsa import sarsa
from sarsa import sarsa_eduardo
from sarsa import sarsa_iterative
from matplotlib import pyplot as plt

# goal_reward = argv[1]
# pit_reward = argv[2]
# step_cost = argv[3]
# giveup_cost = argv[4]
# trials = argv[5]
# epsilon = argv[6]

# 5 -2 -0.1 -3 10000 0.1
goal_reward = 100
pit_reward = -2
step_cost = -0.1
num_iterations = 10000
epsilon = 0.1
giveup_cost = -2

p = 'P'
g = 'G'
r = 'O'
num_rows = 6
num_cols = 7
state_map = [[r, r, r, r, r, r, r],
             [r, r, r, r, r, r, r],
             [r, r, p, p, r, r, r],
             [r, p, g, r, r, p, r],
             [r, r, p, p, p, r, r],
             [r, r, r, r, r, r, r]]

# The learning rate determines to what extent newly acquired information overrides old information.
# A factor of 0 will make the agent not learn anything, while a factor of 1 would make
#  the agent consider only the most recent information.
alpha = 0.4  # Learning Rate

# The discount factor determines the importance of future rewards. A factor
# of 0 makes the agent "opportunistic" by only considering current rewards,
# while a factor approaching 1 will make it strive for a long-term high reward.
# If the discount factor meets or exceeds 1, the Q values may diverge.
gamma = 0.5  # Discount Factor


# Initialize the map
grid = gd.Grid(state_map, goal_reward, pit_reward, step_cost, giveup_cost, epsilon)

rewards = list()
for iteration in range(num_iterations):

    # Get a random node
    node = grid.get_rand_node()  # type: Node
    # point = gd.Point(1, 5)
    # node = grid.get_node(point)

    # Run sarsa() from that node
    # sarsa(node, alpha, gamma)
    # sarsa_iterative(node, alpha, gamma)
    reward = sarsa_eduardo(node, alpha, gamma)
    grid.clear_actions()
    # if type(reward) == float:
    #     rewards.append(reward)


    # DEGBUG: print resulting grid
    # gd.print_grid(grid)
    # print()


# ####### Print out results ####### #
# def chunks(l, n):
#     """Yield successive n-sized chunks from l."""
#     for i in range(0, len(l), n):
#         yield l[i:i + n]
#
# r = chunks(rewards, 100)
# x = list()
# y = list()
# for index, val in enumerate(r):
#     print(sum(val), index)
#     x.append(index)
#     y.append(sum(val))
#
# plt.scatter(x, y, marker='.')
# plt.show()


# Print Results
gd.print_grid(grid)
gd.print_grid(grid, view_reward=True)


