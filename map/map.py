class Map(object):
    """docstring for Map"""
    def __init__(self):
        self.pit_reward = 0
        self.goal_reward = 0
        self.move_reward = 0
        self.giveup_reward = 0

        self.rewards = None
        self.position_x = 0
        self.position_y = 0
        self.initialize_map()

    def initialize_map(self):
        self.rewards = [[0, 0,  0,  0,  0,  0, 0],
                    [0, 0,  0,  0,  0,  0, 0],
                    [0, 0, -1, -1,  0,  0, 0],
                    [0, -1, 1,  0,  0, -1, 0],
                    [0, 0, -1, -1, -1,  0, 0],
                    [0, 0,  0,  0,  0,  0, 0]]

    def move(self):
        return

    def print_map(self):
        return

    def initialize_rewards(self):
        self.position_x = 0
        self.position_y = 0
        return


