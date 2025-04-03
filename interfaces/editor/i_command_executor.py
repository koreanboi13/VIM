from abc import ABC, abstractmethod
from typing import Optional

class ICommandExecutor(ABC):
    @abstractmethod
    def execute_command(self, command: str) -> bool:
        pass

    @abstractmethod
    def register_command(self, command: str, handler: callable) -> None:
        pass
