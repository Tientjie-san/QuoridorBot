from environments.Quoridor import Quoridor



""""Load memories"""
"""Load models"""


""" """
current_player = None
best_player = None

iteration = 0

gamne_over = False
for i in range(1,4):

    print(f"Simulating game {i}")
    quoriodor_env = Quoridor((9, 9), 1)
    actions = quoriodor_env.legal_actions(quoriodor_env.player1_pos, quoriodor_env.player2_pos)
    game_over = False
    print(quoriodor_env.current_state())

    while not game_over:
        actions = quoriodor_env.legal_actions(quoriodor_env.player1_pos, quoriodor_env.player2_pos)
        print(actions)
        action = input().split(', ')
        if len(action) == 2:
            action = tuple([int(ele) for ele in action])
        else:
            action = (int(action[0]), int(action[1]), action[2])

        state = quoriodor_env.step(action)
        print(state)
        game_over = state["game_over"]

    quoriodor_env.reset()
    """ """


