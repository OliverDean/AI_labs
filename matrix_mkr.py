import random

def generate_random_matrix(n):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j] = random.randint(1, 100)  # distances between 1 and 100
            matrix[j][i] = matrix[i][j]
    return matrix

matrix_list = [generate_random_matrix(100) for _ in range(2)]

for idx, matrix in enumerate(matrix_list, 1):
    print(f"Matrix {idx}:")
    for row in matrix:
        print(row)
    print("\n")
