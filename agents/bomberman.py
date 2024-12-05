from mesa import Agent
from agents.road import RoadAgent
from agents.rock import RockAgent
from agents.bomb import BombAgent
from agents.metal import MetalAgent

class BombermanAgent(Agent):
    def __init__(self, unique_id, model, search_strategy, depth):
        super().__init__(unique_id, model)
        self.search_strategy = search_strategy
        self.depth = depth
        self.path_to_exit = []
        self.has_explored = False
        self.previous_position = None
        self.bomb = None
        self.scape = None

    def step(self):
        self.previous_position = self.pos
        self.visit_cell()

        if not self.bomb:
            from searches.game_theory.alpha_beta_pruning import AlphaBetaPruning
            if isinstance(self.search_strategy, AlphaBetaPruning):
                self.search_strategy.podas = 0
                _, next_pos = self.search_strategy.search(turn = "B", depth=self.depth)
                total = self.search_strategy.podas
                print(f"En el paso actual se hicieron en total {total} podas para BOMBERMAN")
                if next_pos:
                    x, y = next_pos
                    agents_in_new_cell = self.model.grid[x][y]

                    if any(isinstance(agent, RockAgent) for agent in agents_in_new_cell):
                        self.bomb = BombAgent(self.pos, self.model)
                        self.model.grid.place_agent(self.bomb, self.pos)
                        self.model.schedule.add(self.bomb)
                        self.scape = self.bomb.timer
                        self.bomb = self.pos
                    else:
                        self.model.grid.move_agent(self, next_pos)

            else:
                if not self.has_explored:
                    start_position = (self.pos[0], self.pos[1])
                    self.path_to_exit = self.search_strategy.search(start_position, self, diagonal=False)
                    self.has_explored = bool(self.path_to_exit)
                    if self.has_explored:
                        next_pos = self.path_to_exit.pop(0)
                        self.model.grid.move_agent(self, next_pos)

                if self.path_to_exit:
                    next_pos = self.path_to_exit.pop(0)
                    x, y = next_pos
                    agents_in_new_cell = self.model.grid[x][y]

                    if any(isinstance(agent, RockAgent) for agent in agents_in_new_cell):
                        self.bomb = BombAgent(self.pos, self.model)
                        self.model.grid.place_agent(self.bomb, self.pos)
                        self.model.schedule.add(self.bomb)
                        self.path_to_exit.insert(0, next_pos)
                        self.scape = self.bomb.timer
                        self.bomb = self.pos
                    else:
                        self.model.grid.move_agent(self, next_pos)
        else:
            self.move_away_from_bomb()

    def visit_cell(self):
        agents_in_position = self.model.grid.get_cell_list_contents([self.pos])
        for agent in agents_in_position:
            if isinstance(agent, RoadAgent):
                agent.is_visited = True
                break

    def move_away_from_bomb(self):
        if self.scape > 0:
            self.scape -= 1
            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            best_position = None
            max_distance = -1

            for direction in directions:
                new_x = self.pos[0] + direction[0]
                new_y = self.pos[1] + direction[1]
                new_position = (new_x, new_y)

                if (
                    0 <= new_x < self.model.grid.width
                    and 0 <= new_y < self.model.grid.height
                    and new_position != self.previous_position
                ):
                    agents_in_new_cell = self.model.grid[new_x][new_y]

                    if not any(isinstance(agent, (MetalAgent, RockAgent)) for agent in agents_in_new_cell):
                        distance_to_bomb = abs(new_x - self.bomb[0]) + abs(new_y - self.bomb[1])

                        if distance_to_bomb > max_distance:
                            max_distance = distance_to_bomb
                            best_position = new_position

            if best_position:
                self.path_to_exit.insert(0, self.pos)
                self.model.grid.move_agent(self, best_position)

        else:
            self.bomb = None