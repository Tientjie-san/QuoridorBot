import random
from .Agent import Agent


class RandomAgent(Agent):

    def action(self, observation):
        print(f"Random Agent observation: {observation}")
        legal_actions = list(observation["legal_actions"])
        return random.choice(legal_actions)
