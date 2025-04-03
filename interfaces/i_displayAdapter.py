from abc import ABC, abstractmethod
class IDisplayAdapter(ABC):
    @abstractmethod
    def init(self) -> None: 
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

    @abstractmethod
    def get_key(self) -> str:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod        
    def refresh(self) -> None:
        pass

    @abstractmethod
    def get_window_size(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def move_cursor(self, y: int, x: int) -> None:
        pass

    @abstractmethod
    def write_line(self, y: int, x: int, text: str, attr=None) -> None: 
        pass

    @abstractmethod
    def write_status_line(self, text: str) -> None:
        pass