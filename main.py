from sys import argv
import sarsa


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
trials = 1
epsilon = 0.1

num_rows = 6
num_cols = 7
state_map = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 9, 9, 0, 0, 0],
             [0, 9, 1, 0, 0, 9, 0],
             [0, 0, 9, 9, 9, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]

state_rep = {9: {'SYM': 'P', 'STATE': 'PIT'},
             1: {'SYM': 'G', 'STATE': 'GOAL'},
             3: {'SYM': '<', 'STATE': 'LEFT'},
             5: {'SYM': '>', 'STATE': 'RIGHT'},
             4: {'SYM': 'v', 'STATE': 'DOWN'}}


# The learning rate determines to what extent newly acquired information overrides old information.
# A factor of 0 will make the agent not learn anything, while a factor of 1 would make
#  the agent consider only the most recent information.
learning_rate = 0.5

# The discount factor determines the importance of future rewards. A factor
# of 0 makes the agent "opportunistic" by only considering current rewards,
# while a factor approaching 1 will make it strive for a long-term high reward.
# If the discount factor meets or exceeds 1, the {\displaystyle Q} Q values may diverge.
discount_factor = 0.5