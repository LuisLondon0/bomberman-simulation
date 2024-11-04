from searches.search_strategy import SearchStrategy
from agents.goal import GoalAgent
from agents.road import RoadAgent
from agents.enemy import EnemyAgent
import heapq
from typing import List, Tuple

class UniformCostSearch(SearchStrategy):
    def __init__(self):
        self.priority_queue = []
        self.visited = set()
        self.cost_so_far = {}
        self.step_count = 0
        self.index = 0

    def search(self, start: Tuple[int, int], agent, diagonal: bool = False) -> List[Tuple[int, int]]:
        heapq.heappush(self.priority_queue, (0, self.index, start, [start]))
        self.cost_so_far[start] = 0
        self.index += 1

        while self.priority_queue:
            current_cost, _, current, path = heapq.heappop(self.priority_queue)
            
            agents_in_cell = agent.model.grid[current[0]][current[1]]
            if any(isinstance(a, GoalAgent) for a in agents_in_cell):
                return path
            
            if current not in self.visited:
                agent.model.grid[current[0]][current[1]][0].visit_order = self.step_count
                self.step_count += 1
                self.visited.add(current)

                if diagonal:
                    directions = [
                        (0, 1, False), (1, 1, True), (1, 0, False), (1, -1, True),
                        (0, -1, False), (-1, -1, True), (-1, 0, False), (-1, 1, True)
                    ]
                else:
                    directions = [(-1, 0, False), (0, 1, False), (1, 0, False), (0, -1, False)]

                for direction in directions:
                    new_x, new_y, is_diagonal = current[0] + direction[0], current[1] + direction[1], direction[2]
                    new_position = (new_x, new_y)

                    if (
                        0 <= new_x < agent.model.grid.width
                        and 0 <= new_y < agent.model.grid.height
                        and new_position not in self.visited
                    ):
                        agents_in_new_cell = agent.model.grid[new_x][new_y]
                        if all(isinstance(a, (RoadAgent, GoalAgent, EnemyAgent)) for a in agents_in_new_cell):
                            new_cost = current_cost + (13 if is_diagonal else 10)
                            if new_position not in self.cost_so_far or new_cost < self.cost_so_far[new_position]:
                                self.cost_so_far[new_position] = new_cost
                                heapq.heappush(self.priority_queue, (new_cost, self.index, new_position, path + [new_position]))
                                self.index += 1

        return []