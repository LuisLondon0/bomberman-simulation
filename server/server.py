from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization import Choice

#Import agents
from agents.bomberman import BombermanAgent
from agents.goal import GoalAgent
from agents.metal import MetalAgent
from agents.road import RoadAgent
from agents.rock import RockAgent
from agents.enemy import EnemyAgent
from agents.bomb import BombAgent
from agents.blast import BlastAgent

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
    elif type(agent) is BombAgent:
        portrayal["Shape"] = "assets/images/bomb.png"
        portrayal["Layer"] = 0
    elif type(agent) is BlastAgent:
        portrayal["Shape"] = "assets/images/blast.png"
        portrayal["Layer"] = 0
    elif type(agent) is GoalAgent:
        portrayal["Shape"] = "assets/images/goal.png"
        portrayal["Layer"] = 0
    elif type(agent) is EnemyAgent:
        portrayal["Shape"] = "assets/images/enemy.png"
        portrayal["Layer"] = 0
    elif type(agent) is MetalAgent:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "gray"
        portrayal["r"] = 1
        portrayal["Layer"] = 1
    elif type(agent) is RoadAgent:
        if agent.visit_order:
            portrayal["text"] = str(agent.visit_order)
            portrayal["text_color"] = "black" 
        if agent.is_visited:
            portrayal["Color"] = "goldenrod"
        else:
            portrayal["Color"] = "green"
        portrayal["Shape"] = "rect"
        portrayal["r"] = 1
        portrayal["Layer"] = 0
    elif type(agent) is RockAgent:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "firebrick"
        portrayal["r"] = 1
        portrayal["Layer"] = 1

    return portrayal

def create_server(map):
    height = len(map)
    width = len(map[0])
    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

    params = {
        "height": height,
        "width": width,
        "map": map,
        "search_strategy": Choice(
            "Search strategy",
            value="DFS",
            choices=["DFS", "BFS", "UCS", "A*", "HILL_CLIMBING", "BEAM_SEARCH"],
        ),
        "heuristic": Choice(
            "Heuristic (Informed searches only)",
            value="Manhattan",
            choices=["Manhattan", "Euclidean"],
        )
    }

    server = ModularServer(LabyrinthModel, [grid], "Bomberman", params)
    server.port = 8521
    return server