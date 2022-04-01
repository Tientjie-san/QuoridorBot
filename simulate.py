from environments import QuoridorEnv
from agents import HumanAgent, RandomAgent

TOTAL_SIMULATIONS = 3


def simulate(env, agent1, agent2):
    env = env(agent2)
    total_reward = 0

    for i in range(TOTAL_SIMULATIONS):

        print(f"Simulating game {i+1}")
        done = False
        obs = env.reset()

        while not done:

            action = agent1.action(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward

    print(f"total reward: {total_reward}")
    print(f"win_percentage: {total_reward/(TOTAL_SIMULATIONS*10) *100}%")


simulate(QuoridorEnv, HumanAgent(), RandomAgent())
