#Searches import
from searches.informed_searchs import a_star, hill_climbing, beam_search
from searches.uninformed_searchs import dfs, bfs, uniform_cost
from searches.game_theory import alpha_beta_pruning

class SearchFactory:
    @staticmethod
    def create_search(type, heuristic_type=None, model=None):
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
        elif type == "BEAM_SEARCH":
            return beam_search.BeamSearch(heuristic_type.lower(), 2)
        elif type == "ALPHA_BETA_PRUNING":
            return alpha_beta_pruning.AlphaBetaPruning(model)
        else:
            raise ValueError("Invalid search type")