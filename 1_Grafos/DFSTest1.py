#Depth
#nodos de 0 a N
adj_matrix = [[0, 1, 1, 0, 1, 1], 
              [0, 0, 0, 0, 0, 1], 
              [1, 1, 0, 0, 0, 0], 
              [0, 1, 1, 0, 0, 0], 
              [0, 1, 0, 1, 0, 0], 
              [1, 1, 0, 0, 0, 0]]

def neighbors(graph, a):
    neighbors = []
    for i in range(len(graph[a])):
        if graph[a][i] == 1:
            neighbors.append(i)
    return neighbors


def dfs(graph, visiting, visited):
    visited.append(visiting)
    for j in neighbors(adj_matrix, visiting):
        if j not in visited:
            dfs(adj_matrix, j, visited)
    return len(visited) == len(adj_matrix)

def main_dfs(grafico, visiting):
    visitado = []
    return dfs(grafico, visiting, visitado)

print(main_dfs(adj_matrix, 0))
