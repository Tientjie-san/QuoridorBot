from .Graph import Graph
import copy


class Player:
    def __init__(self, pos: tuple, goal: int):
        self.pos = pos
        self.fences = 10
        self.placed_fences = []
        self.goal = goal


class Quoridor:

    def __init__(self):
        self.board: Graph = self.create_board()
        self.player_1: Player = Player((0, 4), 8)
        self.player_2: Player = Player((8, 4), 0)
        self.current_player: Player = self.player_1
        self.waiting_player: Player = self.player_2
        self.fence_pos = []
        self.legal_fences = self.init_possible_fences()
        self.turn = 1

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

    @staticmethod
    def init_possible_fences() -> set:
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

    def move_pawn(self, pos) -> bool:
        if pos not in self.legal_pawn_moves():
            raise ValueError("Illegal pawn move")
        self.current_player.pos = pos
        game_over = self.is_game_over()
        self.switch_players()
        self.turn += 0.5
        return game_over

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
        if self.current_player.fences == 0:
            raise ValueError('Illegal move, no fences left')

        if fence not in self.legal_fences:
            raise ValueError('Illegal move')

        self.fence_pos.append(fence)
        self.current_player.placed_fences.append(fence)
        self.current_player.fences -= 1

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
            if (possible_board.is_reachable(self.current_player.pos, self.current_player.goal) and
                    possible_board.is_reachable(self.waiting_player.pos, self.waiting_player.goal)):
                new_legal_fences.add(fence)
        self.legal_fences = new_legal_fences
        self.switch_players()
        self.turn += 0.5

    def legal_pawn_moves(self) -> set:
        """
        Returns legal pawn moves according to the Quoridor rules
        """
        legal_pawn_moves = []

        legal_pawn_moves.extend(node.key for node in self.board.nodes[self.current_player.pos].connected_to)

        if self.waiting_player.pos in legal_pawn_moves:
            legal_pawn_moves.remove(self.waiting_player.pos)
            opponent_connected = [node.key for node in self.board.nodes[self.waiting_player.pos].connected_to]
            opponent_connected.remove(self.current_player.pos)

            # zelfde rij
            if self.current_player.pos[0] == self.waiting_player.pos[0]:
                if self.current_player.pos[1] > self.waiting_player.pos[1]:
                    pos_behind = (self.waiting_player.pos[0], self.waiting_player.pos[1] - 1)
                else:
                    pos_behind = (self.waiting_player.pos[0], self.waiting_player.pos[1] + 1)
            # zelfde column
            else:
                if self.current_player.pos[0] > self.waiting_player.pos[0]:
                    pos_behind = (self.waiting_player.pos[0] - 1, self.waiting_player.pos[1])
                else:
                    pos_behind = (self.waiting_player.pos[0] + 1, self.waiting_player.pos[1])

            if pos_behind in opponent_connected:
                opponent_connected = [pos_behind]

            legal_pawn_moves.extend(opponent_connected)

        return set(legal_pawn_moves)

    def is_game_over(self):
        return self.current_player.pos[0] == self.current_player.goal

    def reset(self):
        self.board: Graph = self.create_board()
        self.player_1: Player = Player((0, 4), 8)
        self.player_2: Player = Player((8, 4), 0)
        self.current_player: Player = self.player_1
        self.waiting_player: Player = self.player_2
        self.fence_pos = []
        self.legal_fences = self.init_possible_fences()
        self.turn = 1

    def legal_actions(self):
        """
        Returns a set of all legal actions
        """
        if self.current_player.fences != 0:
            return self.legal_pawn_moves().union(self.legal_fences)
        else:
            return self.legal_pawn_moves()

    def switch_players(self):
        waiting = self.current_player
        self.current_player = self.waiting_player
        self.waiting_player = waiting

