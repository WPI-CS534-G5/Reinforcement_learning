from random import randint
import random
import sys
import Node

goal_reward = sys.argv[1]
pit_reward = sys.argv[2]
move_cost = sys.argv[3]
giveup_cost = sys.argv[4]
trials = sys.argv[5]
epsilon = sys.argv[6]




map1 = [[0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0],
       [0, 0, 9, 9, 0, 0, 0],
       [0, 9, 1, 0, 0, 9, 0],
       [0, 0, 9, 9, 9, 0, 0],
       [0, 0, 0, 0, 0, 0, 0]]

rows = 6
columns = 7

#The learning rate determines to what extent newly acquired information overrides old information.
# A factor of 0 will make the agent not learn anything, while a factor of 1 would make the agent consider only the most recent information.
Learning_rate = 0.5
#The discount factor determines the importance of future rewards. A factor of 0 makes the agent "opportunistic" by only considering current rewards,
#while a factor approaching 1 will make it strive for a long-term high reward. If the discount factor meets or exceeds 1, the {\displaystyle Q} Q values may diverge.
Discount_factor = 0.5

#Calculates the updated Q' value
def Q_function(Q1,Q2,Reward):
    return Q1+Learning_rate*(Reward+Discount_factor*Q2-Q1)

# Takes in a coordinate and sets a flag on the map
def set_flag(f, val):
    map[f[0]][f[1]] = val

# Returns random coordinate that does not contain 1 or -1.
def get_rand_position():
    random1 = randint(0, rows - 1)
    random2 = randint(0, columns - 1)
    while(map[random1][random2] == 1 or map[random1][random2] == 9):
        random1 = randint(0, rows - 1)
        random2 = randint(0, columns - 1)
    return random1, random2

# Prints map
def print_map():
    for i in range(rows):
        for j in range(columns):
            if(map[i][j].get_state() == 9):
                print("o", end="")
            elif(map[i][j].get_state() == 1):
                print("X", end="")
            elif(map[i][j].get_state == 2):
                print("^", end="")
            elif(map[i][j].get_state == 3):
                print("<", end="")
            elif(map[i][j].get_state == 4):
                print("v", end="")
            elif(map[i][j].get_state == 5):
                print(">", end="")
            else:
                print(map[i][j].get_state, end="")
            if(j != columns - 1):
                print(" | ", end="")
            else:
                print()




def init_map():
    map = [][]
    for i in range(rows):
        for j in range(columns):

            state = map1[i][j]

            if(map1[i][j]==9):
                reward = pit_reward
            elif(map1[i][j]==1):
                reward = goal_reward
            else:
                reward = 0
            map[i].append(node(j,i,state,reward))


if __name__=="__main__":
    random_position = get_rand_position()
    print("Random Y:", random_position[0])
    print("Random X:", random_position[1])
    set_flag(random_position, "#")
    print_map()
