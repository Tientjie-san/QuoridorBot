# Quoridor 

Reinforcement Learning environment for the game Quoridor

## Functionalities implemented

- simulating games
- add own agent to simulate the game
- add an agent to the environment

### How to start?

run simulate.py

### Notation that the game currently uses:
- pawn_moves and positions are represented by a tuple (row, col) range is 0-8 (I start counting from below)
- fence moves (row, col, orientation) orientation is 'H' for horizontal or 'V' for vertical

Picture to clarify notations:

![img.png](img.png)


TODO
- Translation fucntion that converts my game notation to the "official" game notation: https://quoridorstrats.wordpress.com/notation/
- Environment compatible with OpenGym framework


