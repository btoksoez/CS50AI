"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def is_valid_board(board):
    xs = sum(cell == X for row in board for cell in row)
    os = sum(cell == O for row in board for cell in row)
    if abs(xs - os) > 1:
        return 0
    return 1


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Initial game state
    initial = all(cell == EMPTY for row in board for cell in row)

    # Check if valid board
    if not is_valid_board(board):
        raise Exception("Not valid board")

    # Count empty fields
    count_empty = sum(cell == EMPTY for row in board for cell in row)

    if initial:
        return X
    if count_empty % 2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Check if valid board
    if not is_valid_board(board):
        raise Exception("Not valid board")

    available_actions = set()

    # Add empty fields to available actions
    for row, rows in enumerate(board):
        for column, cell in enumerate(rows):
            if cell == EMPTY:
                available_actions.add((row, column))
    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if valid board
    if not is_valid_board(board):
        raise Exception("Not valid board")

    # Check if valid action
    if action not in actions(board):
        raise Exception("Invalid Action")

    # Make copy
    res_board = copy.deepcopy(board)

    # Unpacking row and column from action tuple
    i, j = action

    # Write new values into board
    if player(board) == X:
        res_board[i][j] = X
    else:
        res_board[i][j] = O
    return res_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check if valid board
    if not is_valid_board(board):
        raise Exception("Not valid board")

    # Check if any player has won
    for player in [X, O]:
        # Horizontal
        if any(all(cell == player for cell in row) for row in board):
            return player
        # Vertical
        if any(all(board[i][j] == player for i in range(3)) for j in range(3)):
            return player
        # Diagonal
        if all(board[i][i] == player for i in range(3)) or all(board[j][2-j] == player for j in range(3)):
            return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == O or winner(board) == X:
        return True
    if not actions(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if not terminal(board):
        raise Exception("Not a terminal state")
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_action = None
    depth = 0

    if terminal(board):
        return None

    if board == initial_state():
        return (0, 0)

    # best action for Player X
    if player(board) == X:
        cur_v = -2
        for action in actions(board):
            action_v, depth = min_value(result(board, action), depth + 1)
            if cur_v < action_v or (cur_v <= action_v and depth < best_depth):
                best_action = action
                best_depth = depth
                cur_v = action_v

    # Best action for Player O
    if player(board) == O:
        cur_v = 2
        for action in actions(board):
            action_v, depth = max_value(result(board, action), depth)
            if cur_v > action_v or (cur_v >= action_v and depth < best_depth):
                cur_v = action_v
                best_action = action
                best_depth = depth

    return best_action


def max_value(board, depth):
    if terminal(board):
        return (utility(board), depth)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action), depth + 1)[0])
    return v, depth


def min_value(board, depth):
    if terminal(board):
        return (utility(board), depth)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action), depth + 1)[0])
    return v, depth
