from mesa import Agent
from agents.blast import BlastAgent
from agents.metal import MetalAgent
from agents.rock import RockAgent

class BombAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.power = 1
        self.timer = self.power + 1
    
    def step(self):
        self.timer -= 1
        if self.timer == 0:
            self.explode()

    def explode(self):
        blast = BlastAgent(self.pos, self.model)
        self.model.grid.place_agent(blast, self.pos)
        self.model.schedule.add(blast)

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for direction in directions:
            for i in range(1, self.power + 1):
                new_x = self.pos[0] + direction[0] * i
                new_y = self.pos[1] + direction[1] * i
                new_position = (new_x, new_y)

                if (
                    0 <= new_x < self.model.grid.width
                    and 0 <= new_y < self.model.grid.height
                ):
                    agents_in_new_cell = self.model.grid[new_x][new_y]
                    metal_found = False
                    rock_found = False

                    for agent in agents_in_new_cell:
                        if isinstance(agent, (RockAgent)):
                            rock_found = True
                            break
                        elif isinstance(agent, MetalAgent):
                            metal_found = True
                            break

                    if metal_found:
                        break

                    if rock_found:
                        blast = BlastAgent(new_position, self.model)
                        self.model.grid.place_agent(blast, new_position)
                        self.model.schedule.add(blast)
                        break
                    
                    blast = BlastAgent(new_position, self.model)
                    self.model.grid.place_agent(blast, new_position)
                    self.model.schedule.add(blast)
                    
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)