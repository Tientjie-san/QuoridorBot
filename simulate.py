from environments import QuoridorEnv
from agents import HumanAgent, RandomAgent

EPISODES = 3


def simulate(env, agent1, agent2):
    env = env(agent2)
    total_reward = 0
    win = 0

    for i in range(EPISODES):

        print(f"Simulating game {i+1}")
        done = False
        obs = env.reset()

        while not done:

            action = agent1.action(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            if reward > 0:
                win += 1
                
    print(f"total reward: {total_reward}")
    print(f"win_percentage: {win/EPISODES *100}%")


simulate(QuoridorEnv, RandomAgent(), RandomAgent())
