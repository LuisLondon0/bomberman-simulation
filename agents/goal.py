from mesa import Agent

class GoalAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)