# connect5.py

ROWS = 7
COLS = 9
WIN_LENGTH = 5

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def is_valid_move(board, col):
    return board[0][col] == 0

def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]

def apply_move(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == 0:
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player for i in range(WIN_LENGTH)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player for i in range(WIN_LENGTH)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player for i in range(WIN_LENGTH)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player for i in range(WIN_LENGTH)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != 0 for col in range(COLS))

def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))
    print()
