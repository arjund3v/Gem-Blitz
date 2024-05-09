from grid_methods import overflow
from data_structures import Queue

# This function duplicates and returns the board. You may find this useful
def copy_board(board):
    current_board = []
    height = len(board)
    for i in range(height):
        current_board.append(board[i].copy())
    return current_board


# this function is your evaluation function for the board
def evaluate_board(board, player):
    # Calculate number of rows and cols
    rows = len(board)
    cols = len(board[0])

    # Winning and loosing state values, they are not the literal score!
    winning = 10000
    losing = -10000

    # These will hold each players score
    player_score = 0
    opponent_score = 0

    # Using two loops, we will calculate the score for the player based off of which player is passed in as an arg
    for i in range(rows):
        for j in range(cols):
            cell_value = board[i][j]
            if player == 1:
                # If the cell is positive, then player 1 gets a score
                if cell_value > 0:
                    player_score += cell_value
                # If the cell is negative, player 2 gets a score
                elif cell_value < 0:
                    opponent_score += abs(cell_value)
            else:
                # If the cell is negative, then player 2 gets a score
                if cell_value < 0:
                    player_score += abs(cell_value)
                # If the cell is positive, then player 1 gets a score
                elif cell_value > 0:
                    opponent_score += cell_value

    # If the player has at least one gem on the board, and the opponent has none we return the winning state
    if player_score > 0 and opponent_score == 0:
        return winning
    # If the player has no gems, and the opponent has at least one gem, we return the loosing state
    elif player_score == 0 and opponent_score > 0:
        return losing
    # If the game is still going on, we just return the difference between scores
    # (the value has no significance, it's just a state value to signify the game is on-going)
    else:
        return player_score - opponent_score


class GameTree:
    class Node:
        def __init__(self, board, depth, player, tree_height=4, score=None, move=None):
            self.board = board
            self.depth = depth
            self.player = player
            self.tree_height = tree_height
            self.children = []
 
            # These two variables are needed later on for the score_nodes function and get_move function
            # to keep track of the move that got us to that node, and to keep track of the max score
            self.score = score
            self.move = move
 
    def __init__(self, board, player, tree_height=4):
        self.player = player
        self.board = copy_board(board)
        self.tree_height = tree_height
        self.root = self.Node(self.board, 0, self.player, self.tree_height)
 
        # Generate tree starts at the root node, expands outwards from there giving us every possible outcome
        self.generate_tree(self.root)
 
        # After the game tree has be created, we score each node (minimax/evaluate board)
        self.score_nodes(self.root, self.root.depth, True if self.player == 1 else False)
 
    def generate_tree(self, node):
        # Base condition (as long as we aren't at the last level, which would indicate leaf nodes)
        if node.depth < self.tree_height:
            # This function will find all possible moves for the player on the current board
            moves = self.find_moves(node.board, node.player)
 
            # For each possible move, we create a child node (think of it as a decision which the player can choose)
            for move in moves:
                # We generate a board based on the move made
                new_board = self.make_move(node, node.board, move)
                # Generate a node for that decision, with the move that got us to this board state
                child_node = self.Node(new_board, node.depth + 1, node.player, self.tree_height, None, move)
                # Add all children (decisions) to the current node
                node.children.append(child_node)
                # Recursive call on the child node (decision), this allows us to form our tree structure
                self.generate_tree(child_node)
 
    def find_moves(self, board, player):
        moves = []
 
        rows = len(board)
        cols = len(board[0])
 
        for i in range(rows):
            for j in range(cols):
                # For maximizing player (player 1)
                if board[i][j] > 0 and player > 0:
                    moves.append((i, j))
                # For minimizing player (player 2)
                elif board[i][j] < 0 and player < 0:
                    moves.append((i, j))
 
        return moves
 
    def make_move(self, node, board, move):
        # The queue here has no significance, just need it for the overflow function
        board_queue = Queue()
 
        row, col = move
 
        # After copying the board, we add to the cell which we want to make the move on
        new_board = copy_board(board)
        new_board[row][col] += self.player
 
        # Once we add the player, we run the overflow process to overflow and overflowing cells
        overflow(new_board, board_queue)
 
        return new_board
 
    def score_nodes(self, node, depth, max_player, alpha=float('-inf'), beta=float('inf')):
        # We check if the depth is 0, or if the node has no children, indicating its a root node or leaf node.
        if self.is_leaf(node) or depth == 0:
            # As per the instructions, we will evaluate the board at the leaf nodes
            return evaluate_board(node.board, self.player if max_player else -self.player)
 
        # This is where the minimax algorithm starts
        if max_player:
            # We set the max_score to -infinity to ensure it is lower than any possible evaluation score
            # (Worst Case)
            max_score = float('-inf')
 
            # We will perform the minimax algorithm on all children of the current node
            for child in node.children:
                # To score an inner node, we chose the best score in the children node.
                # We need to know the score for all the children nodes before we can get
                # the score for the current node
                eval = self.score_nodes(child, depth - 1, False, alpha, beta)
                child.score = eval
 
                # Update max_score to the maximum of its current value and the child's evaluation score
                max_score = max(max_score, eval)
 
                # Alpha beta pruning to reduce the number of nodes which need to be evaluated
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            # Set the current nodes score to the max_score
            # we essentially go to the depth and traverse upwards to get the scores
            node.score = max_score
            return max_score
        else:
            # We set the min_score to infinity to ensure it is higher than any possible evaluation score
            # (Worst Case)
            min_score = float('inf')
 
            # We perform the same algorithm, but we are doing it for the minimizing player
            for child in node.children:
                eval = self.score_nodes(child, depth - 1, True, alpha, beta)
                child.score = eval
                min_score = min(min_score, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            node.score = min_score
            return min_score
 
    def is_leaf(self, node):
        # If the node has no children, that means its a leaf node
        return len(node.children) == 0
 
    # this function is a pure stub.  It is here to ensure the game runs.  Once you complete
    # the GameTree, you will use it to determine what to return.
    def get_move(self):
 
        # Score all nodes in the game tree
        self.score_nodes(self.root, self.tree_height, True if self.player == 1 else False)
 
        # Initialize variables to track the best move and score
        best_move = None
        best_score = float('-inf') if self.player == 1 else float('inf')
 
        # Iterate through all child nodes of the root
        for child in self.root.children:
            # Determine whether to update best_score and best_move based on player's turn
            # Maximizing Player
            if self.player > 0 and child.score > best_score:
                best_score = child.score
                best_move = child.move
            # Minimizing Player
            elif self.player < 0 and child.score < best_score:
                best_score = child.score
                best_move = child.move
 
        return best_move
 
    def clear_tree(self):
        # If the root is none, that means the tree is empty
        if self.root is None:
            return
 
        # This function will perform depth first traversal and clear out children starting at the lowest node
        def recursive_clear(node):
            if node is not None:
                for child in node.children:
                    recursive_clear(child)
                node.children = []
 
        # We start the recursive process by passing the root
        recursive_clear(self.root)
 
        # After the recursion completes, we set the root to none, and the garbage collector will come clean up the free
        # memory.
        self.root = None