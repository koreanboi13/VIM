from abc import ABC, abstractmethod

class IModeHandler(ABC):
    @abstractmethod
    def handle_mode(self, key: str) -> bool:
        pass

    @abstractmethod
    def enter_mode(self) -> None:
        pass

    @abstractmethod
    def exit_mode(self) -> None:
        pass
