from abc import ABC, abstractmethod
from typing import Optional

class IInputHandler(ABC):
    @abstractmethod
    def handle_input(self, key: str) -> bool:
        pass
