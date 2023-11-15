import numpy as np


EMPTY = ' '
PLAYER = '0'
COMPUTER = 'X'
ROW_COUNT = 4
COLUMN_COUNT = 4
WINDOW_LENGTH = 3


def create_board():
    return np.full((ROW_COUNT, COLUMN_COUNT), EMPTY, dtype=str)


def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[ROW_COUNT-1-r][col] == EMPTY:
            return ROW_COUNT-1-r


def drop_piece(board, col, piece):
    row = get_next_open_row(board, col)
    board[row][col] = piece


def winning_move(board, piece):
    # Check horizontal 
    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(ROW_COUNT):
            if np.all(board[r, c:c+WINDOW_LENGTH] == piece):
                return True

    # Check vertical 
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            if np.all(board[r:r+WINDOW_LENGTH, c] == piece):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            if np.all(board[r:r+WINDOW_LENGTH, c:c+WINDOW_LENGTH].diagonal() == piece):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(WINDOW_LENGTH - 1, ROW_COUNT):
            if np.all(np.fliplr(board[r-WINDOW_LENGTH+1:r+1, c:c+WINDOW_LENGTH]).diagonal() == piece):
                return True

    return False


# Evaluate for computer 
def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER
    if piece == PLAYER:
        opponent_piece = COMPUTER

    if np.count_nonzero(window == piece) == WINDOW_LENGTH:
        score += 1000
    elif np.count_nonzero(window == piece) == 3 and np.count_nonzero(window == EMPTY) == 1:
        score += 5
    elif np.count_nonzero(window == piece) == 2 and np.count_nonzero(window == EMPTY) == 2:
        score += 2

    if np.count_nonzero(window == opponent_piece) == 3 and np.count_nonzero(window == EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = [board[r+i][c-i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player):
    valid_locations = [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

    if depth == 0 or winning_move(board, PLAYER) or winning_move(board, COMPUTER) or len(valid_locations) == 0:
        if winning_move(board, COMPUTER):
            return (None, 100000000000000)
        elif winning_move(board, PLAYER):
            return (None, -10000000000000)
        else:
            return (None, 0)
    if maximizing_player:
        value = -np.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()
            drop_piece(b_copy, col, COMPUTER)
            new_score = alpha_beta_pruning(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = np.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()
            drop_piece(b_copy, col, PLAYER)
            new_score = alpha_beta_pruning(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def print_board(board):
    print("-" * (COLUMN_COUNT * 2 + 1))
    for row in board:
        print("|", end="")
        for col in row:
            print(col, end="|")
        print("\n" + "-" * (COLUMN_COUNT * 2 + 1))


def play_game():
    board = create_board()
    game_over = False
    turn = 0

    while not game_over:
        # Player's turn
        if turn == 0:
            col = int(input(f"Player, enter column (0-{COLUMN_COUNT - 1}): "))
            if is_valid_location(board, col):
                drop_piece(board, col, PLAYER)
                if winning_move(board, PLAYER):
                    print("Player wins!")
                    game_over = True
                turn += 1
            else:
                print("Invalid move. Try again.")

        # Computer's turn
        else:
            col, _ = alpha_beta_pruning(board, 35, -np.inf, np.inf, True)
            if is_valid_location(board, col):
                drop_piece(board, col, COMPUTER)
                if winning_move(board, COMPUTER):
                    print("Computer wins!")
                    game_over = True
                turn -= 1

        print_board(board)

        if len([c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]) == 0:
            print("It's a tie!")
            game_over = True


play_game()
