from mesa import Agent

class BombermanAgent(Agent):
    def __init__(self, unique_id, model, search_trategy):
        super().__init__(unique_id, model)
        self.search_strategy = search_trategy

    def step(self):
        pass