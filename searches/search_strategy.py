from abc import ABC, abstractmethod
from typing import List, Tuple
from mesa import Agent

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, start: Tuple[int, int], agent: Agent, diagonal: bool, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        pass