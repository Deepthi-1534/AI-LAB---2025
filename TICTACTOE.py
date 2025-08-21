def print_board(board):
    print(board[0] + " | " + board[1] + " | " + board[2])
    print(board[3] + " | " + board[4] + " | " + board[5])
    print(board[6] + " | " + board[7] + " | " + board[8])


def take_turn(board, player):
    while True:
        try:
            position = int(input(f"{player}'s turn. Choose a position from 1-9: ")) - 1
            if position < 0 or position > 8:
                print("Invalid input. Position must be between 1 and 9.")
            elif board[position] != "-":
                print("Position already taken. Choose a different position.")
            else:
                board[position] = player
                print_board(board)
                break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")


def check_game_over(board):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]

    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] != "-":
            return "win"
    if "-" not in board:
        return "tie"
    return "play"


def main():
    board = ["-"] * 9
    print_board(board)
    current_player = "X"
    game_over = False

    while not game_over:
        take_turn(board, current_player)
        result = check_game_over(board)

        if result == "win":
            print(f"{current_player} wins!")
            game_over = True
        elif result == "tie":
            print("It's a tie!")
            game_over = True
        else:
            current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    main()
