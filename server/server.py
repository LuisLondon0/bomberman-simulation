from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

#Import agents
from agents.bomberman import BombermanAgent
from agents.goal import GoalAgent
from agents.metal import MetalAgent
from agents.road import RoadAgent
from agents.rock import RockAgent

#Import model
from environment.labyrinth import LabyrinthModel

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "w": 1, 
        "h": 1, 
        "Filled": "true",
    }

    if type(agent) is BombermanAgent:
        portrayal["Shape"] = "assets/images/bomberman.png"
        portrayal["Layer"] = 1
    elif type(agent) is GoalAgent:
        portrayal["Shape"] = "assets/images/goal.png"
        portrayal["Layer"] = 1
    elif type(agent) is MetalAgent:
        portrayal["Shape"] = "assets/images/metal.png"
        portrayal["Layer"] = 1
    elif type(agent) is RoadAgent:
        portrayal["Shape"] = "assets/images/road.png"
        portrayal["Layer"] = 0
    elif type(agent) is RockAgent:
        portrayal["Shape"] = "assets/images/rock.png"
        portrayal["Layer"] = 1

    return portrayal

def create_server(map):
    height = len(map)
    width = len(map[0])
    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
    server = ModularServer(LabyrinthModel, [grid], "Bomberman", {"height": height, "width": width, "map": map})
    server.port = 8521
    return server