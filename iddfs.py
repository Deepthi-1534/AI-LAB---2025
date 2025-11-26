from copy import deepcopy

# Define the goal state
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Generate all valid neighbor states by moving the blank tile
def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    row, col = divmod(index, 3)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = state[:]
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append(new_state)

    return neighbors

# Depth-Limited Search
def dls(state, depth, visited):
    if state == GOAL_STATE:
        return [state]
    if depth == 0:
        return None
    visited.add(tuple(state))
    for neighbor in get_neighbors(state):
        if tuple(neighbor) not in visited:
            path = dls(neighbor, depth - 1, visited)
            if path:
                return [state] + path
    return None

# Iterative Deepening DFS
def iddfs(start_state, max_depth=20):
    for depth in range(max_depth):
        visited = set()
        path = dls(start_state, depth, visited)
        if path:
            return path
    return None

# Example start state
start = [1, 2, 3, 4, 0, 6, 7, 5, 8]
solution = iddfs(start)

# Print the solution path
if solution:
    print("Solution found in", len(solution) - 1, "moves:")
    for step in solution:
        print(step[:3])
        print(step[3:6])
        print(step[6:])
        print("-----")
else:
    print("No solution found within depth limit.")
