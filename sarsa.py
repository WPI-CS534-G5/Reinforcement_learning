from node import Node
from random import randrange


state_rep = {9: {'SYM': 'P', 'STATE': 'PIT'},
             1: {'SYM': 'G', 'STATE': 'GOAL'},
             3: {'SYM': '<', 'STATE': 'LEFT'},
             5: {'SYM': '>', 'STATE': 'RIGHT'},
             4: {'SYM': 'v', 'STATE': 'DOWN'},
             0: {'SYM': '0', 'STATE': 'INIT'}}


# Calculates the updated Q' value
def q_function(q1, q2, reward, learning_rate, discount_factor):
    return q1 + learning_rate * (reward + discount_factor * q2 - q1)


# Takes in a coordinate and sets a flag on the map
def set_flag(m, row, col, flag_val):
    m[row][col] = flag_val


# Returns random coordinate that does not contain 1 or -1.
def get_rand_position(m, num_rows, num_cols):
    rand_row = randrange(0, num_rows)
    rand_col = randrange(0, num_cols)
    state = m[rand_row][rand_col]

    if (state == 1) or (state == 9):
        return get_rand_position(m, num_rows, num_cols)

    return [rand_row, rand_col]


def init_map(state_map, goal_reward, pit_reward):
    m = list()  # our new map
    for i, row in enumerate(state_map):
        new_row = list()

        for j, state in enumerate(row):
            reward = 0
            if state == 9:
                reward = pit_reward
            elif state == 1:
                reward = goal_reward

            new_row.append(Node(i, j, state, reward))
        m.append(new_row)
    return m


# Prints map
def print_map(node_map):
    for row in node_map:
        print('| ', end='')

        for node in row:
            state = node.get_state()
            state_symbol = state_rep[state]['SYM']
            print(state_symbol, end='')

            print(' | ', end='')
        print()


if __name__ == "__main__":
    state_map = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 9, 9, 0, 0, 0],
                 [0, 9, 1, 0, 0, 9, 0],
                 [0, 0, 9, 9, 9, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

    rand_pos = get_rand_position(state_map, 6, 7)
    reward_map = init_map(state_map, 5, -2)

    print("Random Y:", rand_pos[0])
    print("Random X:", rand_pos[1])

    set_flag(state_map, rand_pos[0], rand_pos[1], "#")
    print_map(reward_map)
