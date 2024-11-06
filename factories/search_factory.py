#Searches import
from searches.informed_searchs import a_star, hill_climbing
from searches.uninformed_searchs import dfs, bfs, uniform_cost
from searches.game_theory import *

class SearchFactory:
    @staticmethod
    def create_search(type, heuristic_type=None):
        if type == "DFS":
            return dfs.DFS()
        elif type == "BFS":
            return bfs.BFS()
        elif type == "UCS":
            return uniform_cost.UniformCostSearch()
        elif type == "A*":
            return a_star.AStarSearch(heuristic_type.lower())
        elif type == "HILL_CLIMBING":
            return hill_climbing.HillClimbingSearch(heuristic_type.lower())
        else:
            raise ValueError("Invalid search type")