<h1 align="center"> Gem Blitz </h1>
<p align="center">A digital board game to see who fills the board with their gems first!</p>


# How to run
1. Download the repository as a zip or clone it to your local device
2. Extract the contents of the zip folder
3. Using a terminal program, navigate to the downloaded folder
4. Once in the folder, run the command `python3 game.py`
5. A square window should pop up on your screen, enjoy!

# How to play
- The goal of the game is for one of the players to overtake the entire board with their gems
- A player wins if every single gem on the board is one colour, and the player who has that colour is the winner of the game.
- You can play with two real people, or you can play against an AI player with different difficulty levels

# Keybinds
- `u` - To undo the last move you made

# The Nerdy Stuff
Heres some information about approaches I took to implement different features of the game
## Undo Method
- For each move, I would add it to a stack. I binded the undo button the the `u` key, and whenever the key is pressed, we just pop off the stack and revert the board.
## AI Player 
- This was a tricky but fun implementation. To implement a AI player, I created a MASSIVE tree. It has every possibility that this game could ever have, and the tree is generated before the game even starts. Based off of this tree, the AI player makes its moves.
## AI Player Difficulty
- For the difficulty of the AI player, based on the difficulty level, the AI player will go deeper into the tree when making its decision on what move to play, this way it will always be steps ahead of you making it difficult to win. 
