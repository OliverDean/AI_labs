import torch
import random

class MazeAgent:
    def __init__(self):
        # 10x10 maze with 4 possible actions
        self.q_table = torch.zeros((10, 10, 4))
        
        # Parameters for Q-learning
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Exploration rate

        # Map of actions to directions
        self.actions = {0: 'U', 1: 'R', 2: 'D', 3: 'L'}
        self.prev_state = None
        self.prev_action = None

    def reset(self):
        self.prev_state = None
        self.prev_action = None

    def get_next_move(self, x, y):
        if random.random() < self.epsilon:
            # Choose a random action with epsilon probability
            action = random.choice(list(self.actions.keys()))
        else:
            # Choose the action with the highest Q-value
            action = torch.argmax(self.q_table[x, y]).item()

        # If the agent tried this action before and remained in the same state,
        # mark that cell as solid (set its Q-value very low)
        if self.prev_state == (x, y) and self.prev_action is not None:
            self.q_table[self.prev_state[0], self.prev_state[1], self.prev_action] = -1e5

        self.prev_state = (x, y)
        self.prev_action = action

        return self.actions[action]

    def update_q_value(self, reward, new_x, new_y):
        """Update Q-values based on reward and new state."""
        if self.prev_state is None or self.prev_action is None:
            return

        # Q-value update rule
        max_future_q = torch.max(self.q_table[new_x, new_y]).item()
        current_q = self.q_table[self.prev_state[0], self.prev_state[1], self.prev_action].item()
        
        new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * max_future_q)
        self.q_table[self.prev_state[0], self.prev_state[1], self.prev_action] = new_q

# In the testing environment, after calling `get_next_move` and moving the agent,
# you'd need to provide a reward and then call `update_q_value` to let the agent learn.
