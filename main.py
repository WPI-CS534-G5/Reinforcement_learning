from grid import Grid
from grid import Point
from node import Node
import settings as st

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
goal_reward = 5
pit_reward = -4
step_cost = -1
num_iterations = 1000
epsilon = 0.1
giveup_cost = -2

p = st.PIT
g = st.GOAL
r = st.NORM
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
alpha = 0.5  # Learning Rate

# The discount factor determines the importance of future rewards. A factor
# of 0 makes the agent "opportunistic" by only considering current rewards,
# while a factor approaching 1 will make it strive for a long-term high reward.
# If the discount factor meets or exceeds 1, the Q values may diverge.
gamma = 0.6  # Discount Factor


# Initialize the map
grid = Grid(state_map, goal_reward, pit_reward, step_cost, giveup_cost, epsilon)

average_rewards = list()
for iteration in range(1, num_iterations+1):

    # Get a random node
    node = grid.get_rand_node()  # type: Node
    point = node.get_point()  # type: Point
    # print(f'start(row,col): ({point.row_i}, {point.col_i})')

    # Run sarsa() from that node
    reward = sarsa_eduardo(node, alpha, gamma)
    average_rewards.append(grid.get_average_reward())

    print(f'{iteration}, ', end='')
    if iteration % 10 == 0:
        print()
print()

# ####### Print out results ####### #
x = [i for i, v in enumerate(average_rewards)]
plt.scatter(x, average_rewards, marker='.')
plt.title('Average Obtained Reward per Iteration')
plt.xlabel('Average Q-Value')
plt.ylabel('Trial #')
plt.show()

# st.print_grid(grid, best_path=False)
# st.print_grid(grid, best_path=False, view_reward=True)
st.print_grid(grid, best_path=True)
st.print_grid(grid, best_path=True, view_reward=True)

