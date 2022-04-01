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
        self.quoridor: Quoridor = Quoridor()
        super(QuoridorEnv, self).__init__()
        self.agent_env = agent_env
        self.done = False
        self.reward = 0
        self.observation_space = Dict({"pos1": Tuple((Discrete(9), Discrete(9))),
                                       "pos2": Tuple((Discrete(9), Discrete(9))),
                                       "fences1": Discrete(11),
                                       "fences2": Discrete(11)})
        self.action_space = MoveSpace(self.quoridor)

    def step(self, action: tuple):
        """returns new state and reward given current state and action"""
        if len(action) == 2:
            game_over: bool = self.quoridor.move_pawn(action)
            if game_over:
                print("Your agent won the game")
                self.reward = 10

                self.done = True
                observation = self.observe()
                reward = self.reward
                done = self.done
                info = self.observe()

                return observation, reward, done, info
        else:
            self.quoridor.add_fence(action)

        # opponents turn:

        opp_action = self.agent_env.action(self.observe())
        if len(opp_action) == 2:
            game_over: bool = self.quoridor.move_pawn(opp_action)
            if game_over:
                print("Opposing agent won the game")
                self.reward = -10
                self.done = True

        else:
            self.quoridor.add_fence(opp_action)

        observation = self.observe()
        reward = self.reward
        done = self.done
        info = self.observe()

        return observation, reward, done, info

    def reset(self):
        """"Resets the Quoridor enviroment"""
        print("resetting env")
        self.quoridor.reset()
        self.done = False
        self.reward = 0
        return self.observe()

    def close(self):
        """close pygame"""
        pass

    def render(self):
        """game vizualisation"""
        self.quoridor.print_internal_board()

    def observe(self):
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
            "agent_pos": self.quoridor.current_player.pos,
            "opposing_agent_pos": self.quoridor.waiting_player.pos,
            "fences1": self.quoridor.current_player.fences,
            "fences2": self.quoridor.waiting_player.fences,
            "fence_pos": self.quoridor.fence_pos,
            "game_over": self.done,
            "reward": self.reward,
            "legal_actions": self.quoridor.legal_actions(),
            "turn": int(self.quoridor.turn)
        }


# from stable_baselines3.common.env_checker import check_env
#
#
# env = QuoridorEnv()
# check_env(env)