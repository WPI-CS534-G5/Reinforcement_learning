from sys import argv
import sarsa



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
