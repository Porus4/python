import heapq

class Node:
    def __init__(self, g_value, h_value, i_cell, j_cell, shuffled_matrix):
        self.g_value = g_value
        self.h_value = h_value
        self.i_cell = i_cell
        self.j_cell = j_cell
        self.shuffled_matrix = shuffled_matrix

    def __lt__(self, other):
        return (self.g_value + self.h_value) < (other.g_value + other.h_value)

    def __eq__(self, other):
        return (self.g_value + self.h_value) == (other.g_value + other.h_value)

def is_visited(visited, new_matrix):
    for visited_matrix in visited:
        if visited_matrix == new_matrix:
            return True
    return False

def find_shuffled_matrix(original, i, j, new_i, new_j):
    shuffled = [row[:] for row in original]
    shuffled[i][j], shuffled[new_i][new_j] = shuffled[new_i][new_j], shuffled[i][j]
    return shuffled

def compare(original, shuffled):
    count = 0
    for i in range(len(original)):
        for j in range(len(original[0])):
            if original[i][j] != shuffled[i][j]:
                count += 1
    return count

def bfs(source, original, goal_state):
    row = len(original)
    col = len(original[0])
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]
    visited = [original]
    paths = []
    pq = [(0, source)]

    while pq:
        _, curr_node = heapq.heappop(pq)
        paths.append(curr_node)

        if curr_node.shuffled_matrix == goal_state:
            return curr_node, paths

        for k in range(4):
            new_i = dx[k] + curr_node.i_cell
            new_j = dy[k] + curr_node.j_cell

            if 0 <= new_i < row and 0 <= new_j < col:
                neighbour = Node(0, 0, 0, 0, [])
                new_mat = [row[:] for row in curr_node.shuffled_matrix]
                i,j = curr_node.i_cell,curr_node.j_cell
                new_mat[i][j],new_mat[new_i][new_j]=new_mat[new_i][new_j],new_mat[i][j]
                neighbour.shuffled_matrix = new_mat
                neighbour.g_value = curr_node.g_value + 1
                neighbour.h_value = compare(neighbour.shuffled_matrix, goal_state)
                neighbour.i_cell = new_i
                neighbour.j_cell = new_j
                if neighbour.h_value==0:
                    node = Node(neighbour.g_value,0,neighbour.i_cell,neighbour.j_cell,neighbour.shuffled_matrix)
                    paths.append(node)
                    return node,paths

                if not is_visited(visited, neighbour.shuffled_matrix):
                    heapq.heappush(pq, (neighbour.g_value + neighbour.h_value, neighbour))
                    visited.append(neighbour.shuffled_matrix)

row = 3
col = 3
original = [[1, 2, 3], [-1, 4, 6], [7, 5, 8]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, -1]]
source = Node(0, compare(original, goal_state), 0, 0, original)

for i in range(row):
    for j in range(col):
        if original[i][j] == -1:
            source.i_cell = i
            source.j_cell = j
            break

target, paths = bfs(source, original, goal_state)

print("h_value:", target.h_value)
print("g_value:", target.g_value)
print("\nPath_of_Matrices:\n")

for node in paths:
    curr_matrix = node.shuffled_matrix
    for row in curr_matrix:
        print(*row)
    print()