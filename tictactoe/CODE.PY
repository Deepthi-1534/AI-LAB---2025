import math

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def is_moves_left(board):
    for row in board:
        if "_" in row:
            return True
    return False

def evaluate(board):
    for row in board:
        if row[0] == row[1] == row[2]:
            if row[0] == 'X':
                return 10
            elif row[0] == 'O':
                return -10
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == 'X':
                return 10
            elif board[0][col] == 'O':
                return -10
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'X':
            return 10
        elif board[0][0] == 'O':
            return -10
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == 'X':
            return 10
        elif board[0][2] == 'O':
            return -10
    return 0

def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)
    if score == 10 or score == -10:
        return score
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = 'X'
                    val = minimax(board, depth+1, False, alpha, beta)
                    best = max(best, val)
                    alpha = max(alpha, best)
                    board[i][j] = "_"
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = 'O'
                    val = minimax(board, depth+1, True, alpha, beta)
                    best = min(best, val)
                    beta = min(beta, best)
                    board[i][j] = "_"
                    if beta <= alpha:
                        break
        return best

def find_best_move(board, player):
    best_val = -math.inf if player == 'X' else math.inf
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = player
                move_val = minimax(board, 0, player == 'O', -math.inf, math.inf)
                board[i][j] = "_"
                if player == 'X':
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (i, j)
                else:
                    if move_val < best_val:
                        best_val = move_val
                        best_move = (i, j)
    return best_move

def main():
    board = [
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_']
    ]
    turn = 'X'
    while True:
        print_board(board)
        if not is_moves_left(board):
            print("Draw!")
            break
        if evaluate(board) == 10:
            print("X wins!")
            break
        if evaluate(board) == -10:
            print("O wins!")
            break
        if turn == 'X':
            i, j = find_best_move(board, 'X')
            print(f"AI X moves to ({i}, {j})")
            board[i][j] = 'X'
            turn = 'O'
        else:
            valid = False
            while not valid:
                try:
                    user_input = input("Enter your move (row and column, 0-based, separated by space): ")
                    i, j = map(int, user_input.strip().split())
                    if 0 <= i < 3 and 0 <= j < 3 and board[i][j] == "_":
                        board[i][j] = 'O'
                        valid = True
                    else:
                        print("Invalid move. Try again.")
                except:
                    print("Invalid input format. Try again.")
            turn = 'X'

if __name__ == "__main__":
    main()