# mcts.py

import math
import random
import copy
import connect5

class Node:
    def __init__(self, board, player, parent=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = connect5.get_valid_moves(board)

    def uct_select_child(self):
        return max(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))

    def expand(self):
        move = self.untried_moves.pop()
        next_board = copy.deepcopy(self.board)
        connect5.apply_move(next_board, move, self.player)
        next_player = 3 - self.player
        child = Node(next_board, next_player, parent=self)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

def simulate(board, player):
    current_player = player
    sim_board = copy.deepcopy(board)

    while True:
        valid_moves = connect5.get_valid_moves(sim_board)
        if not valid_moves:
            return 0.5  # Draw
        move = random.choice(valid_moves)
        connect5.apply_move(sim_board, move, current_player)
        if connect5.check_win(sim_board, current_player):
            return 1 if current_player == player else 0
        if connect5.is_draw(sim_board):
            return 0.5
        current_player = 3 - current_player

def mcts(board, player, iterations=1000):
    root = Node(board, player)

    for _ in range(iterations):
        node = root

        # Selection
        while node.untried_moves == [] and node.children != []:
            node = node.uct_select_child()

        # Expansion
        if node.untried_moves:
            node = node.expand()

        # Simulation
        result = simulate(node.board, node.player)

        # Backpropagation
        while node is not None:
            node.update(result if node.player != player else 1 - result)
            node = node.parent

    # Best move selection
    best_child = max(root.children, key=lambda c: c.visits)
    for i in range(connect5.COLS):
        temp_board = copy.deepcopy(board)
        if connect5.apply_move(temp_board, i, player) and temp_board == best_child.board:
            return i
    return random.choice(connect5.get_valid_moves(board))
