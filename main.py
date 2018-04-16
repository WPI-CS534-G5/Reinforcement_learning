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
goal_reward = 10
pit_reward = -4
step_cost = -0.1
num_iterations = 1000
epsilon = 0.1
giveup_cost = -4

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
alpha = 0.4  # Learning Rate

# The discount factor determines the importance of future rewards. A factor
# of 0 makes the agent "opportunistic" by only considering current rewards,
# while a factor approaching 1 will make it strive for a long-term high reward.
# If the discount factor meets or exceeds 1, the Q values may diverge.
gamma = 0.6  # Discount Factor


# Initialize the map
grid = Grid(state_map, goal_reward, pit_reward, step_cost, giveup_cost, epsilon)

average_rewards = list()
average_q_values = list()
for iteration in range(1, num_iterations+1):

    # Get a random node
    node = grid.get_rand_node()  # type: Node

    # Run sarsa() from that node
    reward = sarsa_eduardo(node, alpha, gamma)
    # reward = sarsa_iterative(node, alpha, gamma)
    average_rewards.append(reward)
    average_q_values.append(grid.get_average_reward())
print()


# ####### Print out results ####### #
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def scatter_values(y, title, xl, yl):
    x = [i for i, v in enumerate(y)]
    plt.scatter(x, y, marker='.')
    plt.title(title)
    plt.ylabel(yl)
    plt.xlabel(xl)
    plt.show()


def chunk(l, n):
    """Split the list, l, into n chunks"""
    result = list()
    length = len(l)
    for start in range(0, length, n):
        values = list()
        for i in range(start, start + n):
            if i < length:
                values.append(l[i])
        val = sum(values)
        result.append(val)
    return result


# average_rewards = chunk(average_rewards, 100)
# scatter_values(average_rewards, 'Average Obtained Reward per Iteration', 'Iteration #', 'Average Reward')
scatter_values(average_q_values,
               f'Average Obtained Q-Value per Iteration (Alpha {alpha})',
               'Iteration #',
               'Average Q-Value')

# st.print_grid(grid, best_path=False)
# st.print_grid(grid, best_path=False, view_reward=True)
st.print_grid(grid, best_path=True)
st.print_grid(grid, best_path=True, view_reward=True)

