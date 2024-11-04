from mesa import Agent
from agents.road import RoadAgent

class BombermanAgent(Agent):
    def __init__(self, unique_id, model, search_strategy):
        super().__init__(unique_id, model)
        self.search_strategy = search_strategy
        self.path_to_exit = []
        self.has_explored = False
        self.previous_position = None

    def step(self):
        self.previous_position = self.pos
        self.visit_cell()
        if not self.has_explored:
            start_position = (self.pos[0], self.pos[1])
            self.path_to_exit = self.search_strategy.search(start_position, self, diagonal=False)
            self.has_explored = bool(self.path_to_exit)
            next_pos = self.path_to_exit.pop(0)
            self.model.grid.move_agent(self, next_pos)

        if self.path_to_exit:
            next_pos = self.path_to_exit.pop(0)
            self.model.grid.move_agent(self, next_pos)

    def visit_cell(self):
        agents_in_position = self.model.grid.get_cell_list_contents([self.pos])
        for agent in agents_in_position:
            if isinstance(agent, RoadAgent):
                agent.is_visited = True
                break