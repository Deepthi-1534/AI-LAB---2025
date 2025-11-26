import random
import math

# Count attacking pairs
def compute_attacks(state):
    attacks = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

# Generate a neighbor by moving one queen
def get_neighbor(state):
    neighbor = state.copy()
    col = random.randint(0, 3)
    new_row = random.randint(0, 3)
    while neighbor[col] == new_row:
        new_row = random.randint(0, 3)
    neighbor[col] = new_row
    return neighbor

# Simulated Annealing algorithm
def simulated_annealing():
    current = [random.randint(0, 3) for _ in range(4)]
    current_score = compute_attacks(current)
    temperature = 100.0
    cooling_rate = 0.95
    min_temp = 0.01

    while temperature > min_temp and current_score > 0:
        neighbor = get_neighbor(current)
        neighbor_score = compute_attacks(neighbor)
        delta = neighbor_score - current_score

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = neighbor
            current_score = neighbor_score

        temperature *= cooling_rate

    return current

# Print board matrix
def print_board(state):
    board = [['.' for _ in range(4)] for _ in range(4)]
    for col, row in enumerate(state):
        board[row][col] = 'Q'
    for row in board:
        print(' '.join(row))

# Run the algorithm
solution = simulated_annealing()
print("4 Queens Solution (Simulated Annealing):")
print_board(solution)
