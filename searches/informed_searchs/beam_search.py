from searches.search_strategy import SearchStrategy
from agents.goal import GoalAgent
from agents.road import RoadAgent
from agents.enemy import EnemyAgent
from agents.rock import RockAgent
from typing import List, Tuple
from utils.utils import heuristic

class BeamSearch(SearchStrategy):
    def __init__(self, heuristic_type, beam_width: int):
        self.visited = set()
        self.goal = None
        self.heuristic_type = heuristic_type
        self.beam_width = max(1, beam_width)

    def search(self, start: Tuple[int, int], agent, diagonal: bool = False, directions: List[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        if not self.goal:
            self.goal = agent.model.goal_coords

        if directions is None:
            if diagonal:
                directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
            else:
                directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        step = -1
        beam = [(start, 0, [start])]
        aux_bem = []
        priority_order = {direction: idx for idx, direction in enumerate(directions)}
        
        while beam:
            next_beam = []

            for current_position, level, path in beam:
                step += 1
                if current_position == self.goal:
                    return path
                

                self.visited.add(current_position)
                if not agent.model.grid[current_position[0]][current_position[1]][0].visit_order:
                    agent.model.grid[current_position[0]][current_position[1]][0].visit_order = str(level) + " (" + str(step) + ")"

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
                            neighbors.append((heuristic_cost, direction_priority, new_position, path + [new_position]))

                if neighbors:
                    next_beam.extend(neighbors)

            next_beam.sort(key=lambda x: (x[0], x[1]))
            beam = [(pos, level + 1, path) for _, _, pos, path in next_beam[:self.beam_width]]
            aux_bem.extend([(pos, level + 1, path) for _, _, pos, path in next_beam[self.beam_width:]])

            if not beam and aux_bem:
                min_level = min([level for _, level, _ in aux_bem])
                i = 0
                for idx, (pos, level, path) in enumerate(aux_bem):
                    if level == min_level and i < self.beam_width:
                        i += 1
                        beam.append((pos, level, path))
                        aux_bem.pop(idx)
            
            if not beam and not aux_bem:
                return []