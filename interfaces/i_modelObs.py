from abc import ABC, abstractmethod
class IModelObserver(ABC):
    @abstractmethod
    def on_text_changed(self) -> None:
        pass

    @abstractmethod
    def on_cursor_changed(self, line: int, column: int) -> None:
        pass

    @abstractmethod
    def on_mode_changed(self, mode: str) -> None:
        pass

    @abstractmethod
    def on_file_changed(self, filename: str) -> None:
        pass
