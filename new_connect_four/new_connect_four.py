import math


def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    for row in board:
        print('|', end=' ')
        for cell in row:
            print(cell, end=' | ')
        print()
        print('-' * (4 * len(row) + 1))


def is_valid_move(board, column):
    return board[0][column] == ' '


def drop_disc(board, column, player):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            return True
    return False


def undo_move(board, column):
    for row in range(len(board)):
        if board[row][column] != ' ':
            board[row][column] = ' '
            break


def evaluate_position(board, player, window_size):
    score = 0

    # Check horizontally
    for row in range(len(board)):
        for col in range(len(board[0]) - window_size + 1):
            window = board[row][col:col + window_size]
            score += evaluate_window(window, player)

    # Check vertically
    for col in range(len(board[0])):
        for row in range(len(board) - window_size + 1):
            window = [board[row + i][col] for i in range(window_size)]
            score += evaluate_window(window, player)

    # Check diagonally (top-left to bottom-right)
    for row in range(len(board) - window_size + 1):
        for col in range(len(board[0]) - window_size + 1):
            window = [board[row + i][col + i] for i in range(window_size)]
            score += evaluate_window(window, player)

    # Check diagonally (bottom-left to top-right)
    for row in range(window_size - 1, len(board)):
        for col in range(len(board[0]) - window_size + 1):
            window = [board[row - i][col + i] for i in range(window_size)]
            score += evaluate_window(window, player)

    return score


def evaluate_window(window, player):
    opponent = 'X' if player == 'O' else 'O'
    if window.count(player) == len(window) and window.count(' ') == 0:
        return 1
    elif window.count(opponent) == len(window) and window.count(' ') == 0:
        return -1
    else:
        return 0


def minimax(board, depth, alpha, beta, maximizing_player, window_size):
    if depth == 0 or check_winner(board, 'X', window_size) or check_winner(board, 'O', window_size) or is_board_full(
            board):
        return evaluate_position(board, 'O', window_size) - evaluate_position(board, 'X', window_size)

    if maximizing_player:
        max_eval = -math.inf
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                drop_disc(board, col, 'O')
                eval_val = minimax(board, depth - 1, alpha, beta, False, window_size)
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha, eval_val)
                undo_move(board, col)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                drop_disc(board, col, 'X')
                eval_val = minimax(board, depth - 1, alpha, beta, True, window_size)
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                undo_move(board, col)
                if beta <= alpha:
                    break
        return min_eval


def get_best_move(board, window_size):
    best_move = -1
    max_eval = -math.inf
    for col in range(len(board[0])):
        if is_valid_move(board, col):
            drop_disc(board, col, 'O')
            eval_val = minimax(board, 30, -math.inf, math.inf, False, window_size)
            undo_move(board, col)
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = col
    return best_move


def check_winner(board, player, window_size):
    return any(
        evaluate_window([board[row][col] for col in range(len(board[0]))], player) == 1 for row in range(len(board))) or \
        any(evaluate_window([board[row][col] for row in range(len(board))], player) == 1 for col in
            range(len(board[0]))) or \
        any(evaluate_window([board[row + i][col + i] for i in range(window_size)], player) == 1 for row in
            range(len(board) - window_size + 1) for col in range(len(board[0]) - window_size + 1)) or \
        any(evaluate_window([board[row - i][col + i] for i in range(window_size)], player) == 1 for row in
            range(window_size - 1, len(board)) for col in range(len(board[0]) - window_size + 1))


def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)


def play_connect_n(rows, columns, window_size):
    board = create_board(rows, columns)
    player = 'X'

    while True:
        print_board(board)

        if player == 'X':
            column = int(input(f"Player {player}, choose a column (1-{columns}): ")) - 1
            if 0 <= column < columns and is_valid_move(board, column):
                drop_disc(board, column, player)
            else:
                print(f"Invalid column. Choose a column between 1 and {columns}.")
                continue
        else:
            print("AI is thinking...")
            column = get_best_move(board, window_size)
            drop_disc(board, column, player)

        if check_winner(board, player, window_size):
            print_board(board)
            print(f"Player {player} wins!")
            return 1
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            return 0
        else:
            player = 'O' if player == 'X' else 'X'


if __name__ == "__main__":
    rows = int(input("Enter the number of rows: "))
    columns = int(input("Enter the number of columns: "))
    window_size = int(input("Enter the window size (2 or 3): "))

    result = play_connect_n(rows, columns, window_size)

    if result == 1:
        print("You won!")
    elif result == 0:
        print("It's a draw!")
