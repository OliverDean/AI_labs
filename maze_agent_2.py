class MazeAgent:
    def __init__(self):
        self.maze = [[' ' for _ in range(10)] for _ in range(10)]  # Maze layout
        self.visited = {}  # Dictionary to store the depth at which the cell was visited
        self.path = []  # Stack for path: [(move, (x,y))]
        self.depth_limit = 300
        
    def reset(self):
        self.visited.clear()
        self.path.clear()

    def is_blocked(self, x, y):
        # Check if position is out of bounds or blocked in the maze
        if 0 <= x <= 9 and 0 <= y <= 9:
            return self.maze[y][x] == "#"  # Check for walls in the internal maze representation
        return True  # out of bounds is considered blocked

    def update_wall(self, x, y):
        # Set the given position as a wall in the agent's maze representation
        if 0 <= x <= 9 and 0 <= y <= 9:
            self.maze[y][x] = "#"  # Update internal maze representation for walls

    def get_next_move(self, x, y):
        # If we're at the goal, no further action is required
        if (x, y) == (0, 0):
            return None

        # Check if we need to backtrack due to depth limit
        if len(self.path) > self.depth_limit:
            move, _ = self.path.pop()
            reverse_moves = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
            return reverse_moves[move]

        # Check possible moves, prioritizing unvisited and unblocked cells
        moves = [('U', (x, y-1)), ('R', (x+1, y)), ('D', (x, y+1)), ('L', (x-1, y))]
        possible_moves = [(move, next_position) for move, next_position in moves
                        if not self.is_blocked(*next_position) and next_position not in self.visited]

        # If there are unvisited nodes, choose the one with the least visited history
        if possible_moves:
            move, next_position = min(possible_moves, key=lambda x: self.visited.get(x[1], 0))
            self.visited[next_position] = len(self.path)
            self.path.append((move, next_position))
            return move

        # If all adjacent cells are visited or blocked, backtrack
        if self.path:
            move, _ = self.path.pop()
            reverse_moves = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
            return reverse_moves[move]

        return None







def string_to_maze(maze_string):
    return [list(row) for row in maze_string.strip().split('\n')]

def simulate_agent_on_maze(agent, maze):
    x, y = 9, 9  # starting position
    moves = []

    for _ in range(800):  # max moves
        move = agent.get_next_move(x, y)
        if not move:  # agent has reached goal or given up
            break

        nx, ny = x, y  # Calculate next position
        if move == 'U':
            ny -= 1
        elif move == 'D':
            ny += 1
        elif move == 'L':
            nx -= 1
        elif move == 'R':
            nx += 1

        if 0 <= nx < 10 and 0 <= ny < 10 and maze[ny][nx] != '#':
            x, y = nx, ny
            moves.append(move)

            if (x, y) == (0, 0):  # if agent reaches the goal
                moves.append("Goal")
                break

            maze[y][x] = '*'  # Mark the current position as visited in the maze

        else:
            # If the agent hits a wall, update the maze and try again
            agent.update_wall(nx, ny)

    return moves



def test_one():

    
    maze = [
        "..........",
        ".########.",
        ".#......#.",
        ".#.####.#.",
        ".#.#..#.#.",
        ".#.#..#.#.",
        ".#.#..#.#.",
        ".#.#....#.",
        ".#.######.",
        ".#........"
    ]

    agent = MazeAgent()
    agent.reset()

    # Convert the maze into a list of lists for easier manipulation
    maze = [list(row) for row in maze]
    
    moves_made = simulate_agent_on_maze(agent, maze)

    # Mark the path taken by the agent on the maze
    x, y = 9, 9  # starting position
    for move in moves_made:
        new_x, new_y = x, y
        
        if move == 'U':
            new_y -= 1
        elif move == 'D':
            new_y += 1
        elif move == 'L':
            new_x -= 1
        elif move == 'R':
            new_x += 1

        if 0 <= new_x <= 9 and 0 <= new_y <= 9:  # Check boundaries
            x, y = new_x, new_y
            if (x, y) != (0, 0):  # don't overwrite the goal
                maze[y][x] = '*'

    # Print the visual representation of the agent's path
    for row in maze:
        print("".join(row))

    # Print result
    if (x, y) == (0, 0):
        print("Passed")
    else:
        print("Moves made:", " -> ".join(moves_made))
        print("Failed. Closest approach was:", x, y)

test_one()
