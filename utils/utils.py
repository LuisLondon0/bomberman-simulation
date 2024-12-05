import tkinter as tk
from tkinter import filedialog
from typing import Tuple, List
from math import sqrt

def load_map(file_path):
    with open(file_path, 'r') as f:
        map = [line.strip().split(",") for line in f.readlines()]

    map.reverse()
    return map

def get_map_path():
    root = tk.Tk()
    root.withdraw()
    map_path = filedialog.askopenfilename(
        title="Select the map file",
        filetypes=[("Text Files", "*.txt")]
    )
    root.destroy()
    return map_path

def heuristic(current: Tuple[int, int], goal: Tuple[int, int], heuristic_type: str):
    if heuristic_type == 'manhattan':
        return (abs(current[0] - goal[0]) + abs(current[1] - goal[1])) * 10
    elif heuristic_type == 'euclidean':
        return round(sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2) * 10, 2)
    else:
        raise ValueError("Unknown heuristic type. Choose 'manhattan' or 'euclidean'.")
    
def bomberman_heuristic(current: Tuple[int, int], goal: Tuple[int, int], enemy_positions: List[Tuple[int, int]], discount_lambda: float = 0.4) -> float:
    # Distancia Manhattan a la meta
    distance_to_goal = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
    
    # Penalización para cada enemigo, con un descuento inversamente proporcional a la distancia a la meta
    enemy_distance_with_discount = 0
    for enemy_pos in enemy_positions:
        distance_to_enemy = abs(current[0] - enemy_pos[0]) + abs(current[1] - enemy_pos[1])
        # Aplicar descuento inversamente proporcional a la distancia a la meta
        discounted_distance = distance_to_enemy * (1 / (1 + discount_lambda * distance_to_goal))
        enemy_distance_with_discount += discounted_distance
    
    return round(enemy_distance_with_discount, 2)

def enemy_heuristic(enemy_positions: List[Tuple[int, int]], bomberman_position: Tuple[int, int], proximity_threshold: int = 3, extra_cost: float = 5.0) -> float:
    # Inicialización de la distancia total
    total_distance_to_bomberman = 0

    # Evaluar la distancia total de todos los enemigos al Bomberman (distancia Manhattan)
    for enemy_pos in enemy_positions:
        distance_to_bomberman = abs(enemy_pos[0] - bomberman_position[0]) + abs(enemy_pos[1] - bomberman_position[1])
        total_distance_to_bomberman += distance_to_bomberman

        # Evaluar si hay enemigos cercanos y aplicar un coste extra
        for other_enemy_pos in enemy_positions:
            if other_enemy_pos != enemy_pos:
                distance_to_other_enemy = abs(enemy_pos[0] - other_enemy_pos[0]) + abs(enemy_pos[1] - other_enemy_pos[1])
                if distance_to_other_enemy <= proximity_threshold:
                    # Aplicar un coste extra si el enemigo está cerca de otro
                    total_distance_to_bomberman += extra_cost

    # Redondear el valor final de la heurística
    return round(total_distance_to_bomberman, 2)