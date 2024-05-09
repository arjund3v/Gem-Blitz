from game_tree import GameTree

class PlayerTwo:
    def __init__(self, name="P2 Bot", difficulty=2):
        self.name = name
        self.difficulty = difficulty  # New attribute to store difficulty

    def get_name(self):
        return self.name

    def get_play(self, board):
        depth = 2 * self.difficulty

        tree = GameTree(board, -1, tree_height=depth)
        (row, col) = tree.get_move()
        return (row, col)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
