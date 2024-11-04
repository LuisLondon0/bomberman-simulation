from abc import ABC, abstractmethod
from typing import List, Tuple
from mesa import Agent

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, start: Tuple[int, int], agent: Agent, diagonal: bool) -> List[Tuple[int, int]]:
        pass