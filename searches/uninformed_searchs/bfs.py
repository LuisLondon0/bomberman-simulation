from collections import deque
from searches.search_strategy import SearchStrategy
from agents.goal import GoalAgent
from agents.road import RoadAgent
from agents.enemy import EnemyAgent
from agents.rock import RockAgent
from typing import List, Tuple
from mesa import Agent

class BFS(SearchStrategy):
    def __init__(self):
        self.queue = deque()
        self.visited = set()
        self.step_count = 0

    def search(self, start: Tuple[int, int], agent: Agent, diagonal: bool) -> List[Tuple[int, int]]:
        self.queue.append((start, [start]))

        while self.queue:
            current, path = self.queue.popleft()

            agents_in_cell = agent.model.grid[current[0]][current[1]]
            if any(isinstance(a, GoalAgent) for a in agents_in_cell):
                return path

            if current not in self.visited:
                agent.model.grid[current[0]][current[1]][0].visit_order = self.step_count
                self.step_count += 1
                self.visited.add(current)

                directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                if diagonal:
                    directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

                for direction in directions:
                    new_x, new_y = current[0] + direction[0], current[1] + direction[1]
                    new_position = (new_x, new_y)

                    if (
                        0 <= new_x < agent.model.grid.width
                        and 0 <= new_y < agent.model.grid.height
                        and new_position not in self.visited
                    ):
                        agents_in_new_cell = agent.model.grid[new_x][new_y]
                        if all(isinstance(a, (RoadAgent, GoalAgent, EnemyAgent, RockAgent)) for a in agents_in_new_cell):
                            self.queue.append((new_position, path + [new_position]))

        return []