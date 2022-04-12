from games.Quoridor.GUI import GUI

# lijst van games, game wordt omschreven door een his
history = [
        {
            "player1_pos": (0, 4),
            "player2_pos": (8, 4),
            "fences_pos" : [(4,1,'H'), (2,5,'V')]
        },
        {
            "player1_pos": (0, 4),
            "player2_pos": (8, 4),
            "fences_pos" : [(4,1,'H'), (2,5,'V'), (2,5, 'H')]
        },
        {
            "player1_pos": (1, 4),
            "player2_pos": (8, 4),
            "fences_pos" : [(4,1,'H'), (2,5,'V'), (2,5, 'H')]
        }
    ]

gui = GUI(history)
gui.run()

