from environments import QuoridorEnv
from agents import HumanAgent, RandomAgent

TOTAL_SIMULATIONS = 3


def simulate(env, agent1, agent2):

    for i in range(1, TOTAL_SIMULATIONS+1):

        print(f"Simulating game {i}")
        env = env(agent2)
        game_over = False
        obs = env.reset()

        while not game_over:

            action = agent1.action(obs)
            obs, reward, done, info = env.step(action)
            game_over = done

        env.reset()


simulate(QuoridorEnv, HumanAgent(), RandomAgent())
