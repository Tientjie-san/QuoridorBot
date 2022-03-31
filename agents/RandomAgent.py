import random


class RandomAgent:

    def action(self, observation):
        print(f"Random Agent observation: {observation}")
        legal_actions = list(observation["legal_actions"])
        return random.choice(legal_actions)
