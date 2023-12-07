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

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def is_valid_move(board, column):   # Top row is empty
    return board[0][column] == ' '

def switch_player(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'
def drop_disc(board, column, player):
    if not is_valid_move(board, column):
        print("INVALID MOVE. CHECK FOR INVALID MOVE")
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            break
    return board

def undo_move(board, column):
    for row in range(len(board)):
        if board[row][column] != ' ':
            board[row][column] = ' '
            break

def check_winner(board, player, window_size):
    n = len(board)
    m = len(board[0])

    # Check horizontally
    for i in range(n):
        for j in range(m - window_size + 1):
            if all(board[i][j + l] == player for l in range(window_size)):
                return True

    # Check vertically
    for i in range(n - window_size + 1):
        for j in range(m):
            if all(board[i + l][j] == player for l in range(window_size)):
                return True

    # Check diagonally (top-left to bottom-right)
    for i in range(n - window_size + 1):
        for j in range(m - window_size + 1):
            if all(board[i + l][j + l] == player for l in range(window_size)):
                return True

    # Check diagonally (top-right to bottom-left)
    for i in range(n - window_size + 1):
        for j in range(window_size - 1, m):
            if all(board[i + l][j - l] == player for l in range(window_size)):
                return True

    return False


def get_best_move(player, board, window_size):
    best_move = -1  # initialize
    max_eval = -math.inf
    min_eval = math.inf

    for col in range(len(board[0])):
        if is_valid_move(board, col):
            new_board = drop_disc(board, col, player)
            if player == 'X':
                eval_val = minimax(new_board, False, 'X', 'O', window_size)
            else:
                eval_val = minimax(new_board, True, 'X', 'O', window_size)
            undo_move(board, col)
            if player == 'X':
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = col
            elif player == 'O':
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = col
            print("  " + str(eval_val), end=' ')
        else:
            print(" _ ", end=" ")
    print("")
    print("Player's value")
    return best_move

def minimax(board, maximizing_player, max_player, min_player, window_size):
    # check for termination
    if check_winner(board, max_player, window_size):    # X won
        return 1
        """
        if maximizing_player:
            return 1    # X won
        else:
            return -1   # O lost
        """
    elif check_winner(board, min_player, window_size):  # O won
        return -1
        """
        if maximizing_player:
            return -1   # X lost
        else:
            return 1    # O won
        """
    elif is_board_full(board):
        return 0    # Both draw

    if maximizing_player:
        max_eval = -1
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                new_board = drop_disc(board, col, max_player)
                if check_winner(new_board, max_player, window_size):
                    eval = 1000
                else:
                    eval = minimax(new_board, False, 'X', 'O', window_size)
                undo_move(board, col)
                max_eval = max(max_eval, eval)
        return max_eval
    else:   # minimizing player
        min_eval = 1
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                new_board = drop_disc(board, col, min_player)
                if check_winner(new_board, max_player, window_size):
                    eval = -1000
                else:
                    eval = minimax(new_board, True, 'X', 'O', window_size)
                undo_move(board, col)
                min_eval = min(min_eval, eval)
        return min_eval


def play_connect_n(rows, columns, window_size, turn_limit):
    board = create_board(rows, columns)
    player = 'X'

    while True:


        if player == 'X':
            print("Player X's Turn")
            print_board(board)
            column = get_best_move(player, board, window_size)
            board = drop_disc(board, column, player)
        else: # Player is O
            print("Player O's Turn")
            print_board(board)
            column = get_best_move(player, board, window_size)
            board = drop_disc(board, column, player)
        wait = input("Enter a key to continue:")
        if check_winner(board, player, window_size):
            print_board(board)
            print(f"Player {player} wins!")
            return 1
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            return 0
        else:
            player = switch_player(player)



if __name__ == "__main__":
    rows = int(input("Enter the number of rows: "))
    columns = int(input("Enter the number of columns: "))
    window_size = int(input("Enter the window size: "))

    result = play_connect_n(rows, columns, window_size, 200)

    if result == 1:
        print("You won!")
    elif result == 0:
        print("It's a draw!")
