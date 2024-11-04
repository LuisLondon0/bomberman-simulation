#Searches import
from searches.informed_searchs import *
from searches.uninformed_searchs import dfs, bfs, uniform_cost
from searches.game_theory import *

class SearchFactory:
    @staticmethod
    def create_search(type):
        if type == "DFS":
            return dfs.DFS()
        elif type == "BFS":
            return bfs.BFS()
        elif type == "UCS":
            return uniform_cost.UniformCostSearch()
        else:
            raise ValueError("Invalid search type")