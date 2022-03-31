from .Agent import Agent


class HumanAgent(Agent):

    def action(self, observation):

        print(f"Human Agent observation: {observation}")
        action = input().split(', ')
        if len(action) == 2:
            action = tuple([int(ele) for ele in action])
        else:
            action = (int(action[0]), int(action[1]), action[2])
        return action
