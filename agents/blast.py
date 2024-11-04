from mesa import Agent

class BlastAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)