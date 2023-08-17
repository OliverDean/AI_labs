
# NN starting and ending at the castle
# returns the path and the distance


def nearest_neighbors(N, distances):
    distance_matrix = distances
    
    visited = [False] * N
    path = [0]
    visited[0] = True

    while len(path) < N:
        last_city = path[-1]
        nearest_distance = float('inf')
        nearest_city = None

        for i in range(N):
            if not visited[i] and distance_matrix[last_city][i] < nearest_distance:
                nearest_distance = distance_matrix[last_city][i]
                nearest_city = i

        visited[nearest_city] = True
        path.append(nearest_city)

    path.append(0)
    return (path, calculate_distance(distance_matrix, path))

def calculate_distance(distance_matrix, path):
    distance = 0
    for i in range(len(path) - 1):
        distance += distance_matrix[path[i]][path[i+1]]
    distance += distance_matrix[path[-1]][path[0]]
    return distance

# # Example Usage
# N = 3
# distances = [
#     [0, 10, 20],
#     [10, 0, 30],
#     [20, 30, 0]
# ]

# result = nearest_neighbors(N, distances)
# print(result)  # Expected output: ([0, 1, 2, 0], 60)
