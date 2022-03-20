from environments.Quoridor import Quoridor


class QuoridorAgent:
    def __init__(self, env: Quoridor):
        self.state = env.current_state
