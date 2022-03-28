from environments.Quoridor import QuoridorEnv



""""Load memories"""
"""Load models"""


current_player = None
best_player = None

for i in range(1,4):

    print(f"Simulating game {i}")
    quoriodor_env = QuoridorEnv()
    game_over = False
    observation = quoriodor_env.reset()
    print(observation)

    while not game_over:

        actions = observation['legal_actions']
        # print(actions)
        action = input().split(', ')
        if len(action) == 2:
            action = tuple([int(ele) for ele in action])
        else:
            action = (int(action[0]), int(action[1]), action[2])

        obs, reward, done, info = quoriodor_env.step(action)
        print(obs)
        game_over = done

    quoriodor_env.reset()



