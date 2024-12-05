import random
from mesa import Agent
from agents.road import RoadAgent
from agents.goal import GoalAgent
from agents.bomberman import BombermanAgent

class EnemyAgent(Agent):
    def __init__(self, unique_id, model, difficulty):
        super().__init__(unique_id, model)
        self.difficulty = difficulty
        self.search_strategy = None
        self.previous_position = None
        
        if difficulty in ("Medium", "Hard"):
            from searches.game_theory.alpha_beta_pruning import AlphaBetaPruning
            self.search_strategy = AlphaBetaPruning(self.model)

    def step(self):
        self.previous_position = self.pos

        if self.difficulty == "Easy":
            self.random_movement()
        elif self.difficulty in ("Medium", "Hard"):
            self.alpha_beta_movement()

    def random_movement(self):
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

    def alpha_beta_movement(self):
        if self.search_strategy:
            depth = 2 if self.difficulty == "Medium" else 6

            self.search_strategy.podas = 0
            _, next_pos = self.search_strategy.search(turn = "E", depth=depth)
            total = self.search_strategy.podas
            print(f"En el paso actual se hicieron en total {total} podas para ENEMIGO")

            if next_pos:
                x, y = next_pos
                agents_in_new_cell = self.model.grid[x][y]

                if all(isinstance(a, (RoadAgent, GoalAgent, BombermanAgent)) for a in agents_in_new_cell):
                    self.model.grid.move_agent(self, next_pos)