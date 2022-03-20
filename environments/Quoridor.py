import numpy as np
from Graph import Graph


class Quoridor:

    def __init__(self, rows, cols):
        self.board: Graph = Quoridor.create_board()
        self.player1_pos = (4, 5)
        self.player2_pos = (5, 5)
        self.player1_fences = 10
        self.player2_fences = 10

    def print_internal_board(self):
        for node in self.board.nodes.values():
            print(node)

    @staticmethod
    def create_board():
        g = Graph()
        for i in range(9):
            for y in range(9):
                g.add_node((i, y))

        for node in g.nodes:
            g.add_edge(node, (node[0], node[1] + 1))
            g.add_edge(node, (node[0], node[1] - 1))
            g.add_edge(node, (node[0] - 1, node[1]))
            g.add_edge(node, (node[0] + 1, node[1]))

        g.remove_edge((5, 5), (6, 5))

        return g

    def legal_pawn_moves(self):
        legal_pawn_moves = []

        legal_pawn_moves.extend(node.key for node in self.board.nodes[self.player1_pos].connected_to)

        if self.player2_pos in legal_pawn_moves:
            legal_pawn_moves.remove(self.player2_pos)
            player_2_connected = [node.key for node in self.board.nodes[self.player2_pos].connected_to]
            player_2_connected.remove(self.player1_pos)

            # zelfde rij
            if self.player1_pos[0] == self.player2_pos[0]:
                if self.player1_pos[1] > self.player2_pos[1]:
                    pos_behind = (self.player2_pos[0], self.player2_pos[1] - 1)
                else:
                    pos_behind = (self.player2_pos[0], self.player2_pos[1] + 1)
            # zelfde column
            else:
                if self.player1_pos[0] > self.player2_pos[0]:
                    pos_behind = (self.player2_pos[0] - 1, self.player2_pos[1])
                else:
                    pos_behind = (self.player2_pos[0] + 1, self.player2_pos[1])

            if pos_behind in player_2_connected:
                player_2_connected = [pos_behind]

            legal_pawn_moves.extend(player_2_connected)

        return legal_pawn_moves

    def legal_fences(self):
        """"
            Fence rules:
            Fences can't overlap
            Fences have to take up full squares
            A fence cant be placed if it makes the opponent unable to reach the goal
        """
        pass

    def legal_actions(self):
        pass

    def step(self, action):
        """returns new state and reward given current state and action"""

        pass

    def reset(self):
        """"Resets the Quoridor enviroment"""
        pass

    def current_state(self):
        """
        returns given state, state is described with a tuple containing the following information
        - Board
        - position player 1
        - position player 2
        - number of fences player 1
        - number of fences player 2
        """
        pass


game = Quoridor(9, 9)
game.print_internal_board()
print(game.legal_pawn_moves())



