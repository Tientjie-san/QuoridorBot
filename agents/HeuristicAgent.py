from .Agent import Agent
from games.Quoridor.Graph import Graph, Node
from collections import deque
import copy


class HeuristicAgent(Agent):
    """
    Heuristic Agents decides actions by following heuristics:
    - If agent has the shortest path it follows that path
    - if opposing agent has shortest path, set a fence in that path. the fence should maximize the shortest path of the
      opponent
    """
    def __init__(self):
        self.goal = None
        self.opponent_goal = None

    def action(self, observation):
        print(f"Heuristic Agent observation: {observation}")

        if not self.goal:
            if observation['agent_pos'][0] == 0:
                self.goal = 8
                self.opponent_goal = 0
            else:
                self.goal = 0
                self.opponent_goal = 8

        quoridor = observation['game']
        board: Graph = quoridor.board
        # add predecessor and distance attributes to nodes

        my_shortest_path = self.shortest_path(copy.deepcopy(board), observation['agent_pos'],
                                              observation['opposing_agent_pos'], self.goal)
        opponent_shortest_path = self.shortest_path(copy.deepcopy(board), observation['opposing_agent_pos'],
                                                    observation['opposing_agent_pos'], self.opponent_goal)
        if len(my_shortest_path) <= len(opponent_shortest_path):
            action = my_shortest_path[1]
            # follow the shortest path
        else:
            # action = self.best_fence_move(opponent_shortest_path)
            action = my_shortest_path[1]
        return action

    @staticmethod
    def shortest_path(board: Graph, current_pos: tuple, opponent_pos, goal: int) -> list:
        # TODO Plan van aanpak: Input is een copy van het oorspronkelijke board, huidige node en goal. Voeg aan alle
        #  nodes de volgende twee waardes toe: predecessor -> de dichtsbijzijnde node, distance -> afstand van node
        #  ten opzichte van huidige node

        visited = set()
        queue = deque([])

        for node in board.nodes.values():
            node.predecessor = None

        source_node = board.nodes[current_pos]
        opponent_node = board.nodes[opponent_pos]
        queue.append(source_node)
        visited.add(source_node)
        goal_node = None

        while queue:

            # Dequeue a vertex from queue
            node = queue.popleft()
            # check if opponent is in connected, top apply quoridor rules
            if opponent_node in node.connected_to:
                node.connected_to.remove(opponent_node)
                opponent_node.connected_to.remove(node)
                node.connected_to = node.connected_to | opponent_node.connected_to

            # print(f"current node: {node}")
            for neighbour in node.connected_to:

                if neighbour not in visited:
                    # print(f"looking at at: {neighbour}")
                    # visit and add neighbors nodes to the queue
                    visited.add(neighbour)
                    queue.append(neighbour)
                    # update its preceding node
                    neighbour.predecessor = node
                    # stop BFS if the visited node is the end node
                    if neighbour.key[0] == goal:
                        goal_node = neighbour
                        queue.clear()
                        break

        # print(visited_list)
        path = [goal_node.key]
        while goal_node.predecessor:
            goal_node = goal_node.predecessor
            path.insert(0, goal_node.key)

        return path

    @staticmethod
    def best_fence_move(opponent_shortest_path: list) -> tuple:
        """
        Returns most annoying fence move. The most annoying fence move maximizes the shortest path of the opponent.
        If there are equal annoying moves pick a random one.
        """
        #TODO: Zet een fence neer zodat e
        pass

