from mesa import Agent

class RockAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)