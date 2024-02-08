from tictactoe import player, actions, result, winner, terminal, utility, max_value, min_value, minimax

EMPTY = None
x = "X"
o = "O"

board = [[x, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]

print(f"Player: {player(board)}\n")

print(f"Actions: {actions(board)}\n")

#print(f"Result: {result(board, (0, 1))}\n")

print(f"Winner: {winner(board)}\n")

#print(f"Utility: {utility(board)}\n")

print(f"Terminal: {terminal(board)}\n")

print(f"Max-Val: {max_value(board)}\n")
print(f"Min-Val: {min_value(board)}\n")

print(f"Best action: {minimax(board)}\n")


