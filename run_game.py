import json
from games.Quoridor.GUI import GUI


with open('Simulations/shortest_path_vs_random2.json') as f:
    games = json.load(f)

gui = GUI(games)
gui.run()

