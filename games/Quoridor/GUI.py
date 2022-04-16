from turtle import right, update, width
from typing import Tuple
import pygame
from .Quoridor import Quoridor

WIDTH, HEIGHT = 900, 900
ROW, COL = 9, 9
SQUARE_SIZE = WIDTH/COL
FPS = 60

# rgb
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
P1_COLOR = (50, 50, 0)
P2_COLOR = (150, 150, 50)
TILE_COLOR = (220, 220, 220)
PLAYER_SIZE = 30
FENCE_COLOR = (125, 81, 61)
FENCE_LENGTH = 2*SQUARE_SIZE
FENCE_WIDTH = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor")


class GUI:

    def __init__(self, games: list):
        self.games = games
        self.game_index = 0
        self.current_game = games[self.game_index]
        self.turn = 1
        self.player1_pos = self.current_game[self.turn-1]["player1_pos"]
        self.player2_pos = self.current_game[self.turn-1]["player2_pos"]
        self.fences_pos = self.current_game[self.turn-1]["fences_pos"]


    def draw_board(self):
        WINDOW.fill(WHITE)
        for i in range(ROW):
            pygame.draw.line(WINDOW, color=TILE_COLOR, start_pos=(0, i*SQUARE_SIZE), end_pos=(WIDTH, i*SQUARE_SIZE), width=5)

            pygame.draw.line(WINDOW, color=TILE_COLOR, start_pos=(i*SQUARE_SIZE, 0), end_pos=(i*SQUARE_SIZE, HEIGHT), width=5)

    def draw_players(self) -> None:
        
        player1_pos = (self.player1_pos[1] * SQUARE_SIZE + SQUARE_SIZE/2, (ROW-self.player1_pos[0]-1) * SQUARE_SIZE + SQUARE_SIZE/2)
        pygame.draw.circle(WINDOW, color=P1_COLOR, center=player1_pos, radius = PLAYER_SIZE)
        
        player2_pos = (self.player2_pos[1] * SQUARE_SIZE + SQUARE_SIZE/2, (ROW-self.player2_pos[0]-1) * SQUARE_SIZE + SQUARE_SIZE/2)
        pygame.draw.circle(WINDOW, color=P2_COLOR, center=player2_pos, radius = PLAYER_SIZE)
    

    def draw_fences(self) -> None:
        for fence in self.fences_pos:
            x = fence[1]

            # +1 want muur zet je van boven
            y = ROW -(fence[0] + 1)

            if fence[2] == 'H':
                
                start_pos = (x*SQUARE_SIZE, y * SQUARE_SIZE)
                end_pos = (x *SQUARE_SIZE + FENCE_LENGTH, y * SQUARE_SIZE)
                
            if fence[2] == 'V':
                start_pos = ((x+1)*SQUARE_SIZE, y * SQUARE_SIZE)
                end_pos = ((x+1)*SQUARE_SIZE, y * SQUARE_SIZE + FENCE_LENGTH)

            pygame.draw.line(WINDOW, color=FENCE_COLOR, start_pos = start_pos, end_pos = end_pos, width=FENCE_WIDTH)

    def switch_game(self, num: int):
        self.game_index += num
        if self.game_index < 0:
            self.game_index = 0
        if self.game_index >= len(self.games):
            self.game_index = len(self.games) - 1
        self.current_game = self.games[self.game_index]
        self.turn = 1


    def update_positions(self):
        self.player1_pos = self.current_game[self.turn-1]["player1_pos"]
        self.player2_pos = self.current_game[self.turn-1]["player2_pos"]
        self.fences_pos = self.current_game[self.turn-1]["fences_pos"]


    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            # event loop
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        print("right")
                        if self.turn < len(self.current_game):
                            self.turn += 1
                    elif event.key == pygame.K_LEFT:
                        print("left")
                        if self.turn > 1:
                            self.turn -= 1
                    elif event.key == pygame.K_DOWN:
                        self.switch_game(-1)
                    elif event.key == pygame.K_UP:
                        self.switch_game(1)
                    print(self.turn)
                    self.update_positions()

            self.draw_board()
            self.draw_players()
            self.draw_fences()
            pygame.display.update()

        pygame.quit()



