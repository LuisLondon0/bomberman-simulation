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
        self.beam_width = max(1, beam_width)  # Asegurarse de que sea al menos 1

    def search(self, start: Tuple[int, int], agent, diagonal: bool = False, directions: List[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        if not self.goal:
            self.goal = agent.model.goal_coords

        if directions is None:
            if diagonal:
                directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
            else:
                directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        level = -1
        beam = [(start, level, [start])]
        priority_order = {direction: idx for idx, direction in enumerate(directions)}

        agent.model.grid[start[0]][start[1]][0].visit_order = "0"
        
        while beam:
            level += 1
            next_beam = []

            for current_position, _, path in beam:
                self.visited.add(current_position)
                if not agent.model.grid[current_position[0]][current_position[1]][0].visit_order:
                    agent.model.grid[current_position[0]][current_position[1]][0].visit_order = level

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
                            neighbors.append((heuristic_cost, direction_priority, new_position, path + [new_position]))

                # Ordena los vecinos primero por costo heurístico y luego por prioridad de dirección
                neighbors.sort(key=lambda x: (x[0], x[1]))
                
                # Agrega solo los mejores vecinos a `next_beam` según `beam_width`
                next_beam.extend(neighbors[:self.beam_width])

            # Actualiza el beam con los nuevos nodos seleccionados
            beam = [(pos, level, path) for _, _, pos, path in next_beam]

            # Condición de escape en caso de que no haya más opciones
            if not beam and next_beam:
                # Selecciona el mejor camino basado en el costo heurístico y el nivel
                paths_by_level = sorted(
                    ((lvl, heuristic(pos, self.goal, self.heuristic_type), pos, path)
                     for pos, lvl, path in next_beam),
                    key=lambda x: (x[0], x[1])
                )
                if paths_by_level:
                    _, _, best_position, best_path = paths_by_level[0]
                    return best_path

        return []