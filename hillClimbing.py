import random

# Count number of attacking pairs
def compute_attacks(state):
    attacks = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

# Generate neighbors by moving one queen in its column
def get_neighbors(state):
    neighbors = []
    for col in range(len(state)):
        for row in range(len(state)):
            if state[col] != row:
                neighbor = state.copy()
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

# Hill climbing algorithm
def hill_climb():
    current = [random.randint(0, 3) for _ in range(4)]
    current_score = compute_attacks(current)

    while True:
        neighbors = get_neighbors(current)
        next_state = current
        next_score = current_score

        for neighbor in neighbors:
            score = compute_attacks(neighbor)
            if score < next_score:
                next_state = neighbor
                next_score = score

        if next_score == current_score:
            break  # No better neighbor found

        current = next_state
        current_score = next_score

    return current

# Convert solution to matrix
def print_board(state):
    size = len(state)
    board = [['.' for _ in range(size)] for _ in range(size)]
    for col, row in enumerate(state):
        board[row][col] = 'Q'
    for row in board:
        print(' '.join(row))

# Run the algorithm
solution = hill_climb()
print("4 Queens Solution in Matrix Form:")
print_board(solution)
