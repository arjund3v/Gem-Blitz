import pygame
import sys
import math
import copy

from grid_methods import overflow
from data_structures import Queue
from data_structures import Stack
from player1 import PlayerOne
from player2 import PlayerTwo 

class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        return self.current_option

class Board:
    def __init__(self,width,height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height-1][self.width-1] = -1
        self.turn = 0
        

    def get_board(self):
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row,col,player):
        if row >= 0  and row < self.height and col >= 0 and col < self.width and (self.board[row][col]==0 or self.board[row][col]/abs(self.board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player):
        if self.valid_move(row, col, player):
            self.board[row][col] += player
            self.turn += 1
            return True
        return False

    def check_win(self):
        if(self.turn > 0):
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if(self.board[i][j] > 0):
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif(self.board[i][j] < 0):
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if(num_p1 == 0):
                return -1
            if(num_p2== 0):
                return 1
        return 0

    def do_overflow(self,q):
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.board[i].copy())
        numsteps = overflow(self.board, q)
        if(numsteps != 0):
            self.set(oldboard)
        return numsteps
    
    def set(self, newboard):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE+Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.board[row][col] > 0:
                        sprite = p1_sprites
                    else:
                        sprite = p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE //2 - 16
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE //2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE //2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))




# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5

# hate the colours?  there are other options.  Just change the lines below to another colour's file name.  
# the following are available blue, pink, yellow, orange, grey, green
p1spritesheet = pygame.image.load('blue.png')
p2spritesheet = pygame.image.load('pink.png')
p1_sprites = []
p2_sprites = []


player_id = [1 , -1]


for i in range(8):
    curr_sprite = pygame.Rect(32*i,0,32,32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))    


frame = 0

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200,800))

pygame.font.init()
font = pygame.font.Font(None, 36)  # Change the size as needed
bigfont = pygame.font.Font(None, 108)
# Create the game board
# board = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])

status=["",""]
current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)

# Define AI difficulty options
AI_difficulty_options = ["Easy", "Medium", "Hard"]
# Initialize the dropdown menu for AI difficulty
difficulty_dropdown = Dropdown(900, 170, 200, 50, AI_difficulty_options)

# Difficulty mapping to search depth
difficulty_mapping = {
    "Easy": 1,
    "Medium": 2,
    "Hard": 3,
    "Very Hard": 4
}

# Game loop
running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]

# Undo Stack Declaration
undo_stack = Stack()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Implement undo feature when 'u' key is pressed
            if event.key == pygame.K_u and not undo_stack.is_empty():
                # Pop the last board state from the stack and set it as the current board state
                board_state, current_player_state = undo_stack.pop()
                board.board = board_state
                current_player = current_player_state

        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            difficulty_dropdown.handle_event(event)
            choice[0] = player1_dropdown.get_choice()
            choice[1] = player2_dropdown.get_choice()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET    
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE
                # Save the current state before making a new move
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    undo_stack.push((copy.deepcopy(board.board), current_player))

    win = board.check_win()
    if win != 0:
        winner = 1
        if win == -1:
            winner = 2
        has_winner = True

    if not has_winner:
        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next = overflow_boards.dequeue()
                    board.set(next)
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False

                # goes between 0 and 1
                current_player = (current_player + 1) % 2

        else:
            status[0] = "Player " + str(current_player + 1) + "'s turn"
            make_move = False
            if choice[current_player] == 1:
                # Get the current difficulty level from the dropdown
                current_difficulty = difficulty_dropdown.options[difficulty_dropdown.current_option]
                # Lookup the search depth for this difficulty level
                search_depth = difficulty_mapping[current_difficulty]
                # Set the difficulty (search depth) for the AI
                bots[current_player].set_difficulty(search_depth)  # Ensure your bot class supports this method
                # Now get the AI's move based on the updated difficulty
                (grid_row,grid_col) = bots[current_player].get_play(board.get_board())

                status[1] = "Bot chose row {}, col {}".format(grid_row, grid_col)
                if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                       has_winner = True
                       # if p1 makes an invalid move, p2 wins.  if p2 makes an invalid move p1 wins
                       winner = ((current_player + 1) % 2) + 1 
                else:
                    make_move = True
            else:
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True

            if make_move:
                board.add_piece(grid_row, grid_col, player_id[current_player])
                numsteps = board.do_overflow(overflow_boards)
                if numsteps != 0:
                    overflowing = True
                    repeat_step = 0
                else:
                    current_player = (current_player + 1) % 2
                grid_row = -1
                grid_col = -1   

    # Draw the game board
    window.fill(WHITE)
    board.draw(window,frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)
    difficulty_dropdown.draw(window)

    if not has_winner:  
        text = font.render(status[0], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET, 750 ))
        text = font.render(status[1], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET,  700 ))
    else:
        text = bigfont.render("Player " + str(winner)  + " wins!", True, (0, 0, 0))  # Black color
        window.blit(text, (300, 250))



    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()