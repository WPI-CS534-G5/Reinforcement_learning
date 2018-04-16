import settings as st
from grid import Grid
from grid import Point
from sarsa import sarsa_eduardo
from matplotlib import pyplot as plt

# goal_reward = argv[1]
# pit_reward = argv[2]
# step_cost = argv[3]
# giveup_cost = argv[4]
# trials = argv[5]
# epsilon = argv[6]

# 5 -2 -0.1 -3 10000 0.1
goal_reward = 5
pit_reward = -2
step_cost = -0.1
num_iterations = 100
epsilon = 0
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
alpha = 0.8  # Learning Rate (STEP-SIZE)

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
    # node = grid.get_rand_node()  # type: Node
    point = Point(1, 1)
    node = grid.get_node(point)

    # Run sarsa() from that node
    reward = sarsa_eduardo(node, alpha, gamma)
    # reward = sarsa_iterative(node, alpha, gamma)
    average_rewards.append(reward)
    average_q_values.append(grid.get_average_reward())

    print(f'{iteration}, ')
    if iteration % 10 == 0:
        print()


# ####### Print out results ####### #
def plot_values(y, title, xl, yl, scatter=False):
    if scatter:
        plt.scatter(y, marker='.')
    else:
        plt.plot(y)
    plt.title(title)
    plt.ylabel(yl)
    plt.xlabel(xl)
    plt.show()


def chunk(l, n, average=False):
    """Split the list, l, into n chunks"""
    result = list()
    length = len(l)

    # Get Next Slice
    for start in range(0, length, n):
        stop = start + 50
        if stop > length:
            stop = length
        total = sum(l[start:stop])
        if average:
            total = total / (stop - start)
        result.append(total)
    return result


points_per_chunk = 50
label_chunk = f'({points_per_chunk} Iterations per Tick)'
label_parameters = f'(Alpha {alpha}, Gamma {gamma}, Epsilon {epsilon})'

average_rewards = chunk(average_rewards, points_per_chunk, average=True)
plot_values(average_rewards,
            'Average Reward per Iteration ' + label_parameters,
            'Iteration # ' + label_chunk,
            'Average Reward')
average_q_values = chunk(average_q_values, points_per_chunk, average=True)
plot_values(average_q_values,
            'Average Q-Value per Iteration ' + label_parameters,
            'Iteration #' + label_chunk,
            'Average Q-Value')

st.print_grid(grid, best_path=True, view_reward=True)
st.print_grid(grid, best_path=True)

