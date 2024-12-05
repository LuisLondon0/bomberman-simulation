#Agents import
from agents.bomberman import BombermanAgent
from agents.goal import GoalAgent
from agents.metal import MetalAgent
from agents.road import RoadAgent
from agents.rock import RockAgent
from agents.enemy import EnemyAgent

class AgentFactory:
    @staticmethod
    def create_agent(type, unique_id, model, search_strategy = None, difficulty = None, depth = None):
        if type == "bomberman":
            return BombermanAgent(unique_id, model, search_strategy, depth)
        elif type == "goal":
            return GoalAgent(unique_id, model)
        elif type == "metal":
            return MetalAgent(unique_id, model)
        elif type == "road":
            return RoadAgent(unique_id, model)
        elif type == "rock":
            return RockAgent(unique_id, model)
        elif type == "enemy":
            return EnemyAgent(unique_id, model, difficulty)
        else:
            raise ValueError("Invalid agent type")