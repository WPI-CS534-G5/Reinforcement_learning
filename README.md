# Reinforcement_learning
This program uses SARSA (State Action Reward State Action) Reinforcement Learning technique to train a grid-world.
 - Heric Flores Huerta
 - Nikolaos Kalampalikis
 - Eduardo Calle Ortiz


### Run Program


Run: `python3.6 main.py [goal-reward] [pit-reward] [step-cost] [give-up-cost] [#of-iterations] [epsilon]`
Where:
 - Goal Reward is the reward obtained at the goal-state
 - Pit Reward is the reward obtained a pit state
 - Step Cost is the reward for making a move
 - Give-up Cost is the reward for giving up
 - #of Iterations is the number of iterations to train for
 - Epsilon is the exploration probability

Example: `python3.6 main.py 5 -2 -0.1 -3 10000 0.1`