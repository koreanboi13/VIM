from abc import ABC, abstractmethod

class IController(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def handle_input(self, key: str) -> bool:
        pass
