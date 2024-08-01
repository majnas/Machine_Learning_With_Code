from abc import ABC, abstractmethod
class Board(ABC):
    @abstractmethod
    def make_grid(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def get_clicked_pos(self):
        pass