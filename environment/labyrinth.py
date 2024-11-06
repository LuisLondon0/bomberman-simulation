from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from factories.agent_factory import AgentFactory
from factories.search_factory import SearchFactory
from agents.bomberman import BombermanAgent
from agents.goal import GoalAgent
from agents.enemy import EnemyAgent
from agents.blast import BlastAgent
from agents.road import RoadAgent

class LabyrinthModel(Model):
    def __init__(self, width, height, map, search_strategy, heuristic):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.goal_coords = None

        search_strategy = SearchFactory.create_search(search_strategy, heuristic)

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
                    road = AgentFactory.create_agent("road", (x, y), self)
                    self.grid.place_agent(road, (x, y))
                    self.schedule.add(road)
                    rock = AgentFactory.create_agent("rock", (x, y), self)
                    self.grid.place_agent(rock, (x, y))
                    self.schedule.add(rock)
                elif cell == "C_b":
                    road = AgentFactory.create_agent("road", (x, y), self)
                    self.grid.place_agent(road, (x, y))
                    self.schedule.add(road)
                    road.is_visited = True
                    bomberman = AgentFactory.create_agent("bomberman", (x, y), self, search_strategy)
                    self.grid.place_agent(bomberman, (x, y))
                    self.schedule.add(bomberman)
                elif cell == "C_m":
                    road = AgentFactory.create_agent("road", (x, y), self)
                    self.grid.place_agent(road, (x, y))
                    self.schedule.add(road)
                    goal = AgentFactory.create_agent("goal", (x, y), self)
                    self.grid.place_agent(goal, (x, y))
                    self.schedule.add(goal)
                    self.goal_coords = (x, y)
                elif cell == "C_e":
                    road = AgentFactory.create_agent("road", (x, y), self)
                    self.grid.place_agent(road, (x, y))
                    self.schedule.add(road)
                    goal = AgentFactory.create_agent("enemy", (x, y), self)
                    self.grid.place_agent(goal, (x, y))
                    self.schedule.add(goal)

        self.running = True

    def step(self):
        self.schedule.step()
        self.check_conditions()

    def check_conditions(self):
        for cell in self.grid.coord_iter():
            cell_content, (x, y) = cell
            
            bomberman_present = enemy_present = goal_present = blast_present = False
            
            for agent in cell_content:
                if isinstance(agent, BombermanAgent):
                    bomberman_present = True
                elif isinstance(agent, GoalAgent):
                    goal_present = True
                elif isinstance(agent, EnemyAgent):
                    enemy_present = True
                elif isinstance(agent, BlastAgent):
                    blast_present = True
                
                if (bomberman_present and goal_present) or (bomberman_present and enemy_present):
                    self.running = False
                    return
                
            if blast_present:
                agents_to_keep = [agent for agent in cell_content if isinstance(agent, (RoadAgent, GoalAgent, BlastAgent))]
                agents_to_remove = set(cell_content) - set(agents_to_keep)

                for agent in agents_to_remove:
                    self.grid.remove_agent(agent)
                    self.schedule.remove(agent)