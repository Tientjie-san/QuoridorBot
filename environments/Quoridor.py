import random
from .Graph import Graph
import copy


class Quoridor:

    def __init__(self, board_shape: tuple, opponent_agent):
        self.board: Graph = Quoridor.create_board()
        self.player1_pos = (0, 4)
        self.player2_pos = (8, 4)
        self.player1_fences = 10
        self.player2_fences = 10
        self.fence_pos = []
        self.legal_fences = self.init_possible_fences()
        self.game_over = False
        self.reward = 0

    def step(self, action):
        """returns new state and reward given current state and action"""
        if len(action) == 2:
            self.player1_pos = action
            if action[0] == 8:
                print("player 1 won the game")
                self.game_over = True
        else:
            self.add_fence(action)
            self.player1_fences -= 1


        #oppenents turn:
        legal_actions = self.legal_actions(self.player2_pos, self.player1_pos)
        legal_actions = legal_actions['pawn_moves'].union(legal_actions['fence_moves'])
        opp_action = random.choice(list(legal_actions))
        if len(opp_action) == 2:
            self.player2_pos = action
            if action[0] == 0:
                print("player 2 won the game")
                self.game_over = True

        else:
            self.add_fence(opp_action)
            self.player2_fences -= 1
        # self.render()
        return self.current_state()

    def reset(self):
        """"Resets the Quoridor enviroment"""
        self.__init__((9, 9), 1)

    def close(self):
        """close pygame"""
        pass

    def render(self):
        """game vizualisation"""
        self.print_internal_board()

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

        return g

    def init_possible_fences(self) -> set:
        """returns all possible fences at the start of the game"""

        fences = []
        range_row_v_fence = range(1, 9)
        range_row_h_fence = range(0, 8)
        col_range = range(0, 8)

        for j in col_range:
            for i in range_row_v_fence:
                fences.append((i, j, "V"))
            for i in range_row_h_fence:
                fences.append((i, j, "H"))
        return set(fences)

    def add_fence(self, fence: tuple):
        """
        add fence to the board. a fence is represented by a tuple containing the following:
        row index: int
        col index: int
        alignment: H for horizontal, V for vertical

        example: (2,2,H) would put the fence between (2,2) - (3,2) and between (2,3) - (3,3)
        example: (2,2,V) would put the fence between (2,2) - (2,3) and between (1,2) - (1,3)

        Fence rules:
        Fences can't overlap
        Fences have to take up full squares
        A fence cant be placed if it makes the opponent unable to reach the goal
        """
        if fence not in self.legal_fences:
            return "That's ILLEGAL"

        self.fence_pos.append(fence)

        # remove fence from legal fences
        self.legal_fences.remove(fence)

        # place the fence  and remove overlapping fences:
        if fence[2] == "H":
            self.board.remove_edge((fence[0], fence[1]), (fence[0] + 1, fence[1]))
            self.board.remove_edge((fence[0], fence[1] + 1), (fence[0] + 1, fence[1] + 1))
            overlapping_fences = {(fence[0], fence[1] - 1, 'H'), (fence[0], fence[1] + 1, 'H'),
                                  (fence[0] + 1, fence[1], 'V')}
        else:
            self.board.remove_edge((fence[0], fence[1]), (fence[0], fence[1] + 1))
            self.board.remove_edge((fence[0] - 1, fence[1]), (fence[0] - 1, fence[1] + 1))
            overlapping_fences = {(fence[0] - 1, fence[1], 'H'), (fence[0] + 1, fence[1], 'V'),
                                  (fence[0] - 1, fence[1], 'V')}

        self.legal_fences -= overlapping_fences

        new_legal_fences = set()
        for fence in self.legal_fences:
            possible_board = copy.deepcopy(self.board)
            if fence[2] == "H":
                possible_board.remove_edge((fence[0], fence[1]), (fence[0] + 1, fence[1]))
                possible_board.remove_edge((fence[0], fence[1] + 1), (fence[0] + 1, fence[1] + 1))
            else:
                possible_board.remove_edge((fence[0], fence[1]), (fence[0], fence[1] + 1))
                possible_board.remove_edge((fence[0] - 1, fence[1]), (fence[0] - 1, fence[1] + 1))
            if (possible_board.is_reachable(self.player1_pos, 8) and
                    possible_board.is_reachable(self.player2_pos, 0)):
                new_legal_fences.add(fence)
        self.legal_fences = new_legal_fences

    def legal_pawn_moves(self, current_player_pos, opponent_pos) -> list:
        """
        Returns legal pawn moves according to the Quoridor rules
        """
        legal_pawn_moves = []

        legal_pawn_moves.extend(node.key for node in self.board.nodes[current_player_pos].connected_to)

        if opponent_pos in legal_pawn_moves:
            legal_pawn_moves.remove(opponent_pos)
            opponent_connected = [node.key for node in self.board.nodes[opponent_pos].connected_to]
            opponent_connected.remove(current_player_pos)

            # zelfde rij
            if current_player_pos[0] == opponent_pos[0]:
                if current_player_pos[1] > opponent_pos[1]:
                    pos_behind = (opponent_pos[0], opponent_pos[1] - 1)
                else:
                    pos_behind = (opponent_pos[0], opponent_pos[1] + 1)
            # zelfde column
            else:
                if current_player_pos[0] > opponent_pos[0]:
                    pos_behind = (opponent_pos[0] - 1, opponent_pos[1])
                else:
                    pos_behind = (opponent_pos[0] + 1, opponent_pos[1])

            if pos_behind in opponent_connected:
                opponent_connected = [pos_behind]

            legal_pawn_moves.extend(opponent_connected)

        return set(legal_pawn_moves)

    def legal_actions(self, current_player_pos, opponent_pos):
        """
        Returns a dictionary of all legal actions:
        pawn_moves: all pawn moves
        fence_moves: all legal fence moves.
        """
        return {"pawn_moves": self.legal_pawn_moves(current_player_pos, opponent_pos), "fence_moves": self.legal_fences}

    def current_state(self):
        """
        returns given state, state is described with a dictionary containing the following information
        - pos1 : position player 1
        - pos2: position player 2
        - fences1: number of fences player 1
        - fences2: number of fences player 2
        - fence_pos: list of fence positions
        - game_over: boolean
        - reward: int
        """
        return {
            "pos1": self.player1_pos,
            "pos2": self.player2_pos,
            "fences1": self.player1_fences,
            "fences2": self.player2_fences,\
            "fence_pos": self.fence_pos,
            "game_over": self.game_over,
            "reward": self.reward
        }
