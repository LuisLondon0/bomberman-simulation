import random
from mesa import Agent
from agents.road import RoadAgent
from agents.goal import GoalAgent
from agents.bomberman import BombermanAgent

class EnemyAgent(Agent):
    def __init__(self, unique_id, model, search_trategy):
        super().__init__(unique_id, model)
        self.search_strategy = search_trategy
        self.previous_position = None

    def step(self):
        self.previous_position = self.pos
        if self.search_strategy:
            if not self.has_explored:
                start_position = (self.pos[0], self.pos[1])
                self.path_to_exit = self.search_strategy.search(start_position, self, diagonal=False)
                self.has_explored = bool(self.path_to_exit)
                next_pos = self.path_to_exit.pop(0)
                self.model.grid.move_agent(self, next_pos)

            if self.path_to_exit:
                next_pos = self.path_to_exit.pop(0)
                self.model.grid.move_agent(self, next_pos)

        else:
            neighbors = []
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

            for direction in directions:
                new_x, new_y = self.pos[0] + direction[0], self.pos[1] + direction[1]
                new_position = (new_x, new_y)
                if (
                    0 <= new_x < self.model.grid.width
                    and 0 <= new_y < self.model.grid.height
                ):
                    neighbors.append(new_position)

            while neighbors:
                new_position = random.choice(neighbors)

                agents_in_new_cell = self.model.grid[new_position[0]][new_position[1]]
                if all(isinstance(a, (RoadAgent, GoalAgent, BombermanAgent)) for a in agents_in_new_cell):
                    self.model.grid.move_agent(self, new_position)
                    break
                else:
                    neighbors.remove(new_position)