import copy
from searches.search_strategy import SearchStrategy
from typing import List, Tuple, Optional
from agents.bomberman import BombermanAgent
from agents.enemy import EnemyAgent
from agents.goal import GoalAgent
from agents.metal import MetalAgent
from agents.rock import RockAgent
from utils.utils import bomberman_heuristic, enemy_heuristic

class AlphaBetaPruning(SearchStrategy):
    def __init__(self, model):
        """
        Inicializa el algoritmo con una referencia al modelo.
        """
        self.model = model
        self.bomberman_position = None
        self.enemy_positions = []
        self.num_enemies = 0
        self.podas = 0

    def search(self, turn: str, depth: int, current_level: int = 0, alpha: float = float('-inf'), beta: float = float('inf'), matrix: Optional[List[List[List[type]]]] = None) -> Tuple[float, Optional[Tuple[int, int]]]:
        """
        Realiza la búsqueda Alpha-Beta Pruning utilizando la matriz del mapa.
        """
        if matrix is None:  # Inicialización
            matrix = self.model.getMatrix()

        self.update_positions(matrix)

        terminal_value = self.is_terminal(matrix, turn)
        if terminal_value is not None:
            #print(f"[*] Terminal condition met. Evaluation: {terminal_value} for {turn}")
            return terminal_value, None

        if current_level == depth:
            # Si no es terminal pero hemos alcanzado la profundidad
            evaluation = self.evaluate(turn)
            return evaluation, None

        best_move = None

        if turn == "B":  # Maximizing player (Bomberman)
            value = float('-inf')
            aux = 0
            childrens = self.get_legal_moves(matrix, self.bomberman_position)
            for move in childrens:
                aux += 1
                new_matrix = self.simulate_move(matrix, self.bomberman_position, move, "B")
                next_value, _ = self.search("E", depth, current_level + 1, alpha, beta, new_matrix)

                if next_value > value:
                    value = next_value
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    print(f"Se acaba de realizar una poda de {len(childrens) - aux}")
                    self.podas += (len(childrens) - aux)
                    break

            return value, best_move

        elif turn == "E":  # Minimizing player (Enemies)
            value = float('inf')
            for enemy_pos in self.enemy_positions:
                aux = 0
                childrens = self.get_legal_moves(matrix, enemy_pos)
                for move in childrens:
                    aux += 1
                    new_matrix = self.simulate_move(matrix, enemy_pos, move, "E")
                    next_value, _ = self.search("B", depth, current_level + 1, alpha, beta, new_matrix)

                    if next_value < value:
                        value = next_value
                        best_move = move
                    beta = min(beta, value)
                    if alpha >= beta:
                        print(f"Se acaba de realizar una poda de {len(childrens) - aux}")
                        self.podas += (len(childrens) - aux)
                        break

            return value, best_move

    def update_positions(self, matrix):
        """
        Actualiza las posiciones de Bomberman y los enemigos desde la matriz.
        """
        self.bomberman_position = self.find_agent(matrix, "B")
        self.enemy_positions = self.find_all_agents(matrix, "E")
        self.num_enemies = len(self.enemy_positions)

    def find_agent(self, matrix: List[List[List[type]]], agent_type: str) -> Optional[Tuple[int, int]]:
        """
        Encuentra la posición de un agente específico en la matriz.
        """
        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                if agent_type == "B" and any(a == BombermanAgent for a in cell):
                    return x, y
                elif agent_type == "E" and any(a == EnemyAgent for a in cell):
                    return x, y
        return None

    def find_all_agents(self, matrix: List[List[List[type]]], agent_type: str) -> List[Tuple[int, int]]:
        """
        Encuentra todas las posiciones de un tipo de agente en la matriz.
        """
        positions = []
        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                if agent_type == "E" and any(a == EnemyAgent for a in cell):
                    positions.append((x, y))
        return positions

    def is_terminal(self, matrix, turn) -> float:
        """
        Determina si el estado actual es terminal y devuelve el valor correspondiente.
        """
        # Si Bomberman no tiene posición, significa que ha perdido (estado terminal)
        if self.bomberman_position is None:
            return float('-inf')  # Valor bajo para Bomberman (perdió)
        
        x, y = self.bomberman_position

        if turn == "B":
            # Si Bomberman llega a la meta (GoalAgent), es un estado terminal con valor muy alto
            if self.model.goal_coords == self.bomberman_position:
                return 50  # Valor alto para Bomberman (llegó a la meta)
            
            # Si Bomberman está en la misma casilla que un enemigo, es un estado terminal con valor bajo
            for enemy_pos in self.enemy_positions:
                if enemy_pos == self.bomberman_position:
                    return 0  # Valor bajo para Bomberman (lo alcanzó un enemigo)
            
            # Si Bomberman no tiene movimientos disponibles, es un estado terminal
            if not self.get_legal_moves(matrix, self.bomberman_position):
                return 0  # Valor bajo para Bomberman (sin movimientos)
        else:
            # Para los enemigos:
            for enemy_pos in self.enemy_positions:
                # Si el enemigo está en la misma casilla que Bomberman, el estado es terminal para el enemigo con valor bajo
                if enemy_pos == self.bomberman_position:
                    return 0  # Valor bajo para el enemigo (lo atrapó)
                
                # Si un enemigo no tiene movimientos disponibles, es un estado terminal con valor alto
                if not self.get_legal_moves(matrix, enemy_pos):
                    return 10  # Valor alto para el enemigo (sin movimientos)

        # Si no se ha cumplido ninguna condición de terminalidad, el estado no es terminal
        return None  # Estado no terminal

    def evaluate(self, turn: str) -> float:
        """
        Evalúa el estado actual para un turno dado.
        """
        if turn == "B":
            return bomberman_heuristic(self.bomberman_position, self.model.goal_coords, self.enemy_positions)
        elif turn == "E":
            return enemy_heuristic(self.enemy_positions, self.bomberman_position)

    def get_legal_moves(self, matrix, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Obtiene los movimientos legales desde una posición en la matriz.
        """
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        legal_moves = []
        x, y = position

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < len(matrix[0]) and 0 <= new_y < len(matrix):
                # Verifica si la celda no contiene un agente RoadAgent (es decir, es un movimiento legal)
                if all((a != MetalAgent ) for a in matrix[new_y][new_x]):
                    legal_moves.append((new_x, new_y))

        return legal_moves

    def simulate_move(self, matrix: List[List[List[type]]], position: Tuple[int, int], move: Tuple[int, int], turn: str) -> List[List[List[type]]]:
        """
        Simula el movimiento de un agente en la matriz.
        """
        new_matrix = copy.deepcopy(matrix)
        x, y = position
        new_x, new_y = move

        agent_type = BombermanAgent if turn == "B" else EnemyAgent
        new_matrix[y][x] = [a for a in new_matrix[y][x] if a != agent_type]
        new_matrix[new_y][new_x].append(agent_type)

        return new_matrix