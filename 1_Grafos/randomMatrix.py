import random

n = 15  # number of nodes
density = 0.09  # density of edges (percentage)

# create an n x n matrix filled with zeros
adj_matrix = [[0 for j in range(n)] for i in range(n)]

# randomly add edges to the matrix based on the density
for i in range(n):
    for j in range(n):
        if i != j and random.random() < density:
            adj_matrix[i][j] = 1  # add edge from node i to node j

# print the matrix
for row in adj_matrix:
    print(row)
print(adj_matrix)