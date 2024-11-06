from searches.search_strategy import SearchStrategy
from agents.goal import GoalAgent
from agents.road import RoadAgent
from agents.enemy import EnemyAgent
from agents.rock import RockAgent
from typing import List, Tuple
from utils.utils import heuristic

class HillClimbingSearch(SearchStrategy):
    def __init__(self, heuristic_type):
        self.visited = set()
        self.goal = None
        self.heuristic_type = heuristic_type

    def search(self, start: Tuple[int, int], agent, diagonal: bool = False, directions: List[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        if not self.goal:
            self.goal = agent.model.goal_coords

        if directions is None:
            if diagonal:
                directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
            else:
                directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        level = 0
        stack = [(start, level, [start])]
        best_path = []

        priority_order = {direction: idx for idx, direction in enumerate(directions)}

        while stack:
            level += 1
            current_position, _, path = stack.pop()
            self.visited.add(current_position)

            if current_position == self.goal:
                return path

            neighbors = []
            for dx, dy in directions:
                new_x, new_y = current_position[0] + dx, current_position[1] + dy
                new_position = (new_x, new_y)

                if (
                    0 <= new_x < agent.model.grid.width
                    and 0 <= new_y < agent.model.grid.height
                    and new_position not in self.visited
                ):
                    agents_in_new_cell = agent.model.grid[new_x][new_y]
                    if all(isinstance(a, (RoadAgent, GoalAgent, EnemyAgent, RockAgent)) for a in agents_in_new_cell):
                        heuristic_cost = heuristic(new_position, self.goal, self.heuristic_type)
                        direction_priority = priority_order.get((dx, dy), float('inf'))
                        neighbors.append((heuristic_cost, direction_priority, new_position))

            neighbors.sort(key=lambda x: (x[0], x[1]), reverse=True)

            for _, _, neighbor in neighbors:
                if not agent.model.grid[neighbor[0]][neighbor[1]][0].visit_order:
                    stack.append((neighbor, level, path + [neighbor]))
                    agent.model.grid[neighbor[0]][neighbor[1]][0].visit_order = level

        return best_path