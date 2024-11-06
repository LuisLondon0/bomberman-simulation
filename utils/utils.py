import tkinter as tk
from tkinter import filedialog
from typing import Tuple
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