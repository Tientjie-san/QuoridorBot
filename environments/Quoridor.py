import numpy as np
from Graph import Graph


class Quoridor:

    def __init__(self, board_shape: tuple, opponent_agent):
        self.board: Graph = Quoridor.create_board()
        self.player1_pos = (4, 5)
        self.player2_pos = (5, 5)
        self.player1_fences = 10
        self.player2_fences = 10
        self.fence_pos = []

    def step(self, action):
        """returns new state and reward given current state and action"""

        pass

    def reset(self):
        """"Resets the Quoridor enviroment"""
        pass

    def close(self):
        """close pygame"""
        pass

    def render(self):
        """game vizualisation"""
        pass

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

        # for i in range(9):
        #     g.remove_edge((5, i), (6, i))

        return g

    def add_fence(self, fence: tuple):
        """
        add fence to the board. a fence is represented by a tuple containing the following:
        row index: int
        col index: int
        alignment: H for horizontal, V for vertical

        example: (2,2,H) would put the fence between (2,2) - (3,2) and between (2,3) - (3,3)
        example: (2,2,V) would put the fence between (2,2) - (2,3) and between (1,2) - (1,3)
        """
        # check if fence to be placed overlaps, or violates the rule that the goal side has to be reachable.
        pass

    def is_legal_fence(self, fence:tuple) -> bool:



    def legal_pawn_moves(self) -> list:
        """
        Returns legal pawn moves according to the Quoridor rules
        """
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

    def legal_fences(self) -> list:
        """"
            Fence rules:
            Fences can't overlap
            Fences have to take up full squares
            A fence cant be placed if it makes the opponent unable to reach the goal
        """
        fence_moves = []
        for i in range(9):
            possible_board = self.board
            # add fence to possible board
            # check if end is still reachable for both players
            if possible_board.is_reachable(self.player1_pos, 0) and possible_board.is_reachable(self.player2_pos, 8):
                fence_moves.append(1)

        return fence_moves

    def legal_actions(self):
        """
        Returns a dictionary of all legal actions:
        pawn_moves: all pawn moves
        fence_moves: all legal fence moves.
        """
        return {"pawn_moves": self.legal_pawn_moves(), "fence_moves": self.legal_fences()}

    def current_state(self):
        """
        returns given state, state is described with a dictionary containing the following information
        - pos1 : position player 1
        - pos2: position player 2
        - fences1: number of fences player 1
        - fences2: number of fences player 2
        - fence_pos: list of fence positions
        """
        pass


game = Quoridor(9, 9)
print(game.board.is_reachable(game.player1_pos, 8))
print(game.legal_actions())
game.print_internal_board()
