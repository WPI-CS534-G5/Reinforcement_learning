from node import Node
from random import randrange
from sys import argv

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
    state = m[rand_row][rand_col].get_state()

    if (state == 1) or (state == 9):
        return get_rand_position(m, num_rows, num_cols)

    return [rand_col , rand_row]


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


# Decides to move or not based on epsilon
def decide_to_move(epsilon):
    pred = epsilon*100
    rand = randrange(1, 100)
    if(rand > pred):
        return 1
    else:
        return -1

# Checks if the node at x,y exists
def can_move(x,y):
    if((x < 0) or (y < 0) or (x > 6) or (x > 5)):
        return 0
    else:
        return 1

#Returns all the neighbors of a node
def get_neighbors(x,y, map):
    neighbors = []
    if(can_move(x,y+1)):
        neighbors.append(map[x,y+1])
    if(can_move(x,y-1)):
        neighbors.append(map[x,y-1])
    if(can_move(x-1,y)):
        neighbors.append(map[x-1,y])
    if(can_move(x+1,y)):
        neighbors.append(map[x+1,y])
    return neighbors


#Move function, it is not deterministic
def move(x1,y1,x2,y2,map):

    pred = epsilon*100
    rand = randrange(1, 100)

    if




if __name__ == "__main__":

    goal_reward = argv[1]
    pit_reward = argv[2]
    move_cost = argv[3]
    giveup_cost = argv[4]
    trials = argv[5]
    epsilon = argv[6]

    # The learning rate determines to what extent newly acquired information overrides old information.
    # A factor of 0 will make the agent not learn anything, while a factor of 1 would make
    #  the agent consider only the most recent information.
    learning_rate = 0.5

    # The discount factor determines the importance of future rewards. A factor
    # of 0 makes the agent "opportunistic" by only considering current rewards,
    # while a factor approaching 1 will make it strive for a long-term high reward.
    # If the discount factor meets or exceeds 1, the Q values may diverge.
    discount_factor = 0.5

    state_map = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 9, 9, 0, 0, 0],
                 [0, 9, 1, 0, 0, 9, 0],
                 [0, 0, 9, 9, 9, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

    num_rows = 6
    num_cols = 7

    # Initialize the map
    reward_map = init_map(state_map, goal_reward, pit_reward)

    #for all the trials
    for x in range(0, trials):

        # get a random possition
        curr_pos = get_rand_position(reward_map, 6, 7)
        # while your current possition is not on a terminating state
        while(reward_map[curr_pos[0]][curr_pos[1]].get_state() != 1):
            #Takes an epsilon probability that it wont move
            if (decide_to_move(epsilon)<0):
                continue
            #Get all the neighbors of the current possition
            neighbors = get_neighbors(curr_pos[0],curr_pos[1],reward_map)
            #Get the neighbor with the highest q value
            max_coordinates = [curr_pos[0]+1,[curr_pos[1]]
            max_q_value = q_function(reward_map[curr_pos[0]][curr_pos[1]].get_p_value(), reward_map[curr_pos[0]+1][curr_pos[1]].get_p_value(), reward_map[curr_pos[0]+1][curr_pos[1]].get_reward(), learning_rate, discount_factor)
            for n in neighbors:
                if ( q_function(reward_map[curr_pos[0]][curr_pos[1]].get_p_value(), n.get_p_value,n.get_reward,  learning_rate, discount_factor) > max_q_value):
                    max_q_value = q_function(reward_map[curr_pos[0]][curr_pos[1]].get_p_value(), n.get_p_value,n.get_reward,  learning_rate, discount_factor)
                    max_coordinates[0] = n.get_x()
                    max_coordinates[1] = n.get_y()
            move()
            update()

    print_map(reward_map)
