# maze_agent
class MazeAgent:
    def __init__(self):
        self.maze = [[' ' for _ in range(10)] for _ in range(10)]  # Initialize a 10x10 maze representation
        self.prev_x = None
        self.prev_y = None
        self.prev_action = None

    def reset(self):
        self.prev_x = None
        self.prev_y = None
        self.prev_action = None
        self.maze = [[' ' for _ in range(10)] for _ in range(10)]

    def get_next_move(self, x, y):
        # If the previous move did not change the position, mark that direction as a wall
        if self.prev_x == x and self.prev_y == y and self.prev_action:
            if self.prev_action == 'U':
                self.maze[self.prev_y - 1][self.prev_x] = 'W'
            elif self.prev_action == 'R':
                self.maze[self.prev_y][self.prev_x + 1] = 'W'
            elif self.prev_action == 'D':
                self.maze[self.prev_y + 1][self.prev_x] = 'W'
            elif self.prev_action == 'L':
                self.maze[self.prev_y][self.prev_x - 1] = 'W'

        # Check for possible moves and prioritize them
        possible_moves = []

        # Check Up
        if y > 0 and self.maze[y - 1][x] != 'W':
            possible_moves.append('U')
        # Check Right
        if x < 9 and self.maze[y][x + 1] != 'W':
            possible_moves.append('R')
        # Check Down
        if y < 9 and self.maze[y + 1][x] != 'W':
            possible_moves.append('D')
        # Check Left
        if x > 0 and self.maze[y][x - 1] != 'W':
            possible_moves.append('L')

        # If no possible moves, we're trapped (shouldn't happen with a valid maze)
        if not possible_moves:
            return None

        # Prioritize downward and leftward movement to reach (0,0)
        if 'D' in possible_moves:
            action = 'D'
        elif 'L' in possible_moves:
            action = 'L'
        else:
            action = possible_moves[0]  # Pick the first possible action

        self.prev_x = x
        self.prev_y = y
        self.prev_action = action
        return action
