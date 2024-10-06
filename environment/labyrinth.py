from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from factories.agent_factory import AgentFactory
from searches.uninformed_searchs.dfs import dfs
from searches.uninformed_searchs.bfs import bfs
from agents.bomberman import BombermanAgent
from agents.goal import GoalAgent

class LabyrinthModel(Model):
    def __init__(self, width, height, map):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                if cell == "C":
                    road = AgentFactory.create_agent("road", (x, y), self)
                    self.grid.place_agent(road, (x, y))
                    self.schedule.add(road)
                elif cell == "M":
                    metal = AgentFactory.create_agent("metal", (x, y), self)
                    self.grid.place_agent(metal, (x, y))
                    self.schedule.add(metal)
                elif cell == "R":
                    rock = AgentFactory.create_agent("rock", (x, y), self)
                    self.grid.place_agent(rock, (x, y))
                    self.schedule.add(rock)
                elif cell == "C_b":
                    road = AgentFactory.create_agent("road", (x, y), self)
                    self.grid.place_agent(road, (x, y))
                    self.schedule.add(road)
                    search_strategy = dfs()
                    bomberman = AgentFactory.create_agent("bomberman", (x, y), self, search_strategy)
                    self.grid.place_agent(bomberman, (x, y))
                    self.schedule.add(bomberman)
                elif cell == "C_m":
                    goal = AgentFactory.create_agent("goal", (x, y), self)
                    self.grid.place_agent(goal, (x, y))
                    self.schedule.add(goal)

        self.running = True

    def step(self):
        self.schedule.step()
        self.check_bomberman_and_goal()

    def check_bomberman_and_goal(self):
        for cell in self.grid.coord_iter():
            cell_content, (x, y) = cell
            bomberman_present = any(isinstance(agent, BombermanAgent) for agent in cell_content)
            goal_present = any(isinstance(agent, GoalAgent) for agent in cell_content)
            if bomberman_present and goal_present:
                self.running = False
                break