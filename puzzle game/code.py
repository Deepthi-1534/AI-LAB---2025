def get_neighbors_dfs(state):
    neighbors = []
    index = state.index('0')
    row, col = divmod(index, 3)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r, c in moves:
        new_row, new_col = row + r, col + c
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append("".join(new_state))
    return neighbors


def dfs(start_state, goal_state):
    stack = [start_state]
    visited = set()
    parent = {start_state: None}

    while stack:
        current = stack.pop()
        if current == goal_state:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]
        if current not in visited:
            visited.add(current)
            neighbors = get_neighbors_dfs(current)
            neighbors.reverse()
            for neighbor in neighbors:
                if neighbor not in visited:
                    parent[neighbor] = current
                    stack.append(neighbor)
    return None


print("Enter the initial state (enter 3 digits per row, separated by spaces, 0 for empty):")
initial_state_rows = []
for i in range(3):
    row = input(f"Row {i+1}: ").split()
    initial_state_rows.extend(row)
initial_state = "".join(initial_state_rows)

print("\nEnter the goal state (enter 3 digits per row, separated by spaces, 0 for empty):")
goal_state_rows = []
for i in range(3):
    row = input(f"Row {i+1}: ").split()
    goal_state_rows.extend(row)
goal_state = "".join(goal_state_rows)

solution = dfs(initial_state, goal_state)

if solution:
    print("\nDFS solution path:")
    for s in solution:
        print(s[:3])
        print(s[3:6])
        print(s[6:])
        print()
else:
    print("\nNo solution found.")
