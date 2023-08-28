class Node:
    def __init__(self, x, y, g, h):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


class MazeAgent:
    def __init__(self, depth_cutoff=30):
        self.depth_cutoff = depth_cutoff
        self.path = []

    def reset(self):
        self.path = []

    def heuristic(self, x, y):
        # Manhattan distance to goal (0,0)
        return abs(x) + abs(y)

    def find_path(self, start_x, start_y, maze):  # Pass the maze as an additional parameter
        start_node = Node(start_x, start_y, 0, self.heuristic(start_x, start_y))
        open_list = [start_node]  # Use a list instead of a set
        closed_list = set()

        # Precompute the maze dimensions for performance
        width = len(maze[0])
        height = len(maze)

        while open_list:
            current_node = min(open_list, key=lambda o: o.f)
            open_list.remove(current_node)
            closed_list.add((current_node.x, current_node.y))

            # print(f"Expanding node ({current_node.x}, {current_node.y}) with f = {current_node.f}")

            if current_node.x == 0 and current_node.y == 0:
                path = []
                while current_node:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]

            for new_x, new_y in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                node_position = (current_node.x + new_x, current_node.y + new_y)

                if node_position == (0, 0):
                    return [(start_x, start_y), node_position]

                # Use the precomputed width and height for boundary checks
                if not (0 <= node_position[0] < width and 0 <= node_position[1] < height):
                    continue
                
                # print(f"Checking node_position: {node_position} within maze of size {height}x{width}")

                if maze[node_position[1]][node_position[0]] == '#':  # Check for walls
                    continue

                node_g = current_node.g + 1
                if node_g > self.depth_cutoff:
                    continue
                node_h = self.heuristic(node_position[0], node_position[1])
                new_node = Node(node_position[0], node_position[1], node_g, node_h)
                new_node.parent = current_node

                if node_position in closed_list:
                    continue

                # Check if a node with the same position is already in open list with a lower or same cost
                existing_node = next((n for n in open_list if n.x == new_node.x and n.y == new_node.y and n.g <= new_node.g), None)
                if existing_node:
                    continue

                open_list.append(new_node)

        return []

    def get_next_move(self, x, y):
        if not self.path:
            self.path = self.find_path(x, y)

        if len(self.path) > 1:
            next_pos = self.path[1]
            if next_pos[0] > x:
                return 'R'
            elif next_pos[0] < x:
                return 'L'
            elif next_pos[1] > y:
                return 'D'
            else:
                return 'U'
        return None

def string_to_maze(maze_string):
    """Converts a multi-line string representation of a maze to a list of lists."""
    return [list(row) for row in maze_string.strip().split('\n')]

def simulate_agent_on_maze(agent, maze):
    """Simulates the agent moving through the maze and returns the moves made."""
    x, y = 9, 9  # Starting position
    moves = []

    path = agent.find_path(x, y, maze)
    
    # Determine the direction of each move
    for i in range(1, len(path)):
        prev_x, prev_y = path[i - 1]
        next_x, next_y = path[i]
        if next_x > prev_x:
            moves.append('R')
        elif next_x < prev_x:
            moves.append('L')
        elif next_y > prev_y:
            moves.append('D')
        else:
            moves.append('U')

    # Check if the agent reached the goal
    if path[-1] == (0, 0):
        moves.append("Goal")
    
    return moves

def visualize_agent_path(moves, maze):
    """Marks the path taken by the agent on the maze and prints it."""
    x, y = 9, 9  # Starting position
    for move in moves:
        if move == 'U':
            y -= 1
        elif move == 'D':
            y += 1
        elif move == 'L':
            x -= 1
        elif move == 'R':
            x += 1

        # Check boundaries and don't overwrite the goal
        if 0 <= x <= 9 and 0 <= y <= 9 and (x, y) != (0, 0):
            maze[y][x] = '*'

    # Print the visual representation of the agent's path
    for row in maze:
        print("".join(row))

def test_one():
    """Test scenario for the agent to solve the given maze."""
    maze = [
        "..........",
        ".########.",
        "#......#.",  
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
    maze = string_to_maze('\n'.join(maze))

    moves_made = simulate_agent_on_maze(agent, maze)
    visualize_agent_path(moves_made, maze)

    # Check if the agent reached the goal
    if "Goal" in moves_made:
        print("Passed")
    else:
        print("Moves made:", " -> ".join(moves_made))
        print("Failed. Closest approach was:", moves_made[-1])

test_one()
