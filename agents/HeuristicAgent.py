from .Agent import Agent
from games.Quoridor.Graph import Graph


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

        if not self.goal:
            if observation['agent_pos'][0] == 0:
                self.goal = 8
                self.opponent_goal = 0
            else:
                self.goal = 0
                self.opponent_goal = 8

        board: Graph = observation['board']
        board.print_graph()
        my_shortest_path = self.shortest_path(observation['agent_pos'], self.goal)
        opponent_shortest_path = self.shortest_path(observation['opposing_agent_pos'], self.opponent_goal)
        if len(my_shortest_path) <= len(opponent_shortest_path):
            # follow the shortest path
            action = my_shortest_path[0]
        else:
            action = self.best_fence_move(opponent_shortest_path)
        print(f"Heuristic Agent observation: {observation}")
        return action

    @staticmethod
    def shortest_path(position: tuple, goal: int) -> list:
        pass

    @staticmethod
    def best_fence_move(opponent_shortest_path) -> tuple:
        """
        Returns most annoying fence move. The most annoying fence move maximizes the shortest path of the opponent.
        If there are equal annoying moves pick a random one.
        """
        pass


