import json
from games.Quoridor.GUI import GUI


with open('Simulations/simulation_1.json') as f:
    games = json.load(f)

gui = GUI(games)
gui.run()

