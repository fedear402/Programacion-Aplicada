
#Depth
#nodos de 0 a N
adj_matrix = [[0, 1, 1, 0, 1, 0], 
              [0, 0, 0, 0, 0, 0], 
              [1, 1, 0, 0, 0, 0], 
              [0, 1, 1, 0, 0, 0], 
              [0, 1, 0, 1, 0, 0], 
              [0, 0, 0, 0, 0, 0]]

def neighbors(graph, a):
    neighbors = []
    for i in range(len(graph[a])):
        if graph[a][i] == 1:
            neighbors.append(i)
    return neighbors


def dfs(graph, visiting, objective, visited):
    visited.append(visiting)
    for j in neighbors(adj_matrix, visiting):
        if j not in visited:
            dfs(adj_matrix, j, objective, visited)
        else:
            continue
    return objective in visited
#MAIN
def reachable(desde, hasta):
    visited = []
    return dfs(adj_matrix, desde, hasta, visited)

print(reachable(0, 6))
