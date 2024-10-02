from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from factories.agent_factory import AgentFactory

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
                    bomberman = AgentFactory.create_agent("bomberman", (x, y), self)
                    self.grid.place_agent(bomberman, (x, y))
                    self.schedule.add(bomberman)
                elif cell == "S":
                    goal = AgentFactory.create_agent("goal", (x, y), self)
                    self.grid.place_agent(goal, (x, y))
                    self.schedule.add(goal)

        self.running = True

    def step(self):
        self.schedule.step()