import random
import gym
from gym.spaces import Discrete, Dict, Tuple
from games.Quoridor import Quoridor


class MoveSpace(gym.spaces.Space):

    def __init__(self, board):
        self.board = board

    def sample(self):
        legal_actions = self.board.legal_actions(self.board.player1_pos, self.board.player2_pos,
                                                 self.board.player1_fences)
        return random.choice(list(legal_actions))


class QuoridorEnv(gym.Env):

    def __init__(self, agent_env):
        self.board: Quoridor = Quoridor()
        super(QuoridorEnv, self).__init__()
        self.agent_env = agent_env
        self.game_over = False
        self.reward = 0
        self.turn = 1
        self.observation_space = Dict({"pos1": Tuple((Discrete(9), Discrete(9))),
                                       "pos2": Tuple((Discrete(9), Discrete(9))),
                                       "fences1": Discrete(11),
                                       "fences2": Discrete(11)})
        self.action_space = MoveSpace(self.board)

    def step(self, action: tuple):
        """returns new state and reward given current state and action"""
        if len(action) == 2:
            self.board.player1_pos = action
            if self.board.player1_pos[0] == 8:
                print("player 1 won the game")
                self.reward = 10
                self.game_over = True
        else:
            self.board.add_fence(action)
            self.board.player1_fences -= 1

        # opponents turn:

        opp_action = self.agent_env.action(self.observe(is_opp=True))
        if len(opp_action) == 2:
            self.board.player2_pos = opp_action
            if self.board.player2_pos[0] == 0:
                print("player 2 won the game")
                self.reward = 0
                self.game_over = True

        else:
            self.board.add_fence(opp_action)
            self.board.player2_fences -= 1
        # self.render()

        observation = self.observe()
        reward = self.reward
        done = self.game_over
        info = self.observe()
        self.turn += 1
        info['turn'] = self.turn

        return observation, reward, done, info

    def reset(self):
        """"Resets the Quoridor enviroment"""
        print("resetting env")
        self.board.__init__()
        self.game_over = False
        self.reward = 0
        self.turn = 1
        return self.observe()

    def close(self):
        """close pygame"""
        pass

    def render(self):
        """game vizualisation"""
        self.board.print_internal_board()

    def observe(self, is_opp=False):
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

        if is_opp:
            legal_actions = self.board.legal_actions(self.board.player2_pos, self.board.player1_pos,
                                                     self.board.player2_fences)
        else:
            legal_actions = self.board.legal_actions(self.board.player1_pos, self.board.player2_pos,
                                                     self.board.player1_fences)
        return {
            "pos1": self.board.player1_pos,
            "pos2": self.board.player2_pos,
            "fences1": self.board.player1_fences,
            "fences2": self.board.player2_fences,
            "fence_pos": self.board.fence_pos,
            "game_over": self.game_over,
            "reward": self.reward,
            "legal_actions": legal_actions
        }


# from stable_baselines3.common.env_checker import check_env
#
#
# env = QuoridorEnv()
# check_env(env)