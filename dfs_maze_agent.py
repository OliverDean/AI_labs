# dfs_maze_agent
class MazeAgent:
    def __init__(self):
        self.visited = set()  # Set of visited positions
        self.stack = []  # Stack for DFS
        self.prev_x = None
        self.prev_y = None
        self.prev_action = None

    def reset(self):
        self.visited.clear()
        self.stack.clear()
        self.prev_x = None
        self.prev_y = None
        self.prev_action = None

    def get_next_move(self, x, y):
        if (self.prev_x, self.prev_y) == (x, y):
            # Backtrack if we hit a wall
            self.stack.pop()

        self.visited.add((x, y))
        
        # Possible moves from current position
        moves = [('U', (x, y-1)), ('R', (x+1, y)), ('D', (x, y+1)), ('L', (x-1, y))]

        for move, (nx, ny) in moves:
            if 0 <= nx < 10 and 0 <= ny < 10 and (nx, ny) not in self.visited:
                # Mark as visited and push to the stack
                self.visited.add((nx, ny))
                self.stack.append((move, nx, ny))
                
        # If we still have options in the stack, proceed
        if self.stack:
            self.prev_action, self.prev_x, self.prev_y = self.stack[-1]
            return self.prev_action
        else:
            return None  # No available moves, should not happen in a valid maze
