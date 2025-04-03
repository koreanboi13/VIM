from abc import ABC, abstractmethod
from typing import Tuple

class IMovementController(ABC):
    @abstractmethod
    def move_cursor(self, line: int = None, column: int = None) -> None:
        pass

    @abstractmethod
    def move_word_forward(self) -> None:
        pass

    @abstractmethod
    def move_word_backward(self) -> None:
        pass

    @abstractmethod
    def move_to_line_start(self) -> None:
        pass

    @abstractmethod
    def move_to_line_end(self) -> None:
        pass
