from abc import ABC, abstractmethod
from typing import List, Callable, Tuple, Optional
from interfaces.i_modelObs import IModelObserver


class IModel(ABC):
    @abstractmethod
    def add_observer(self, observer: IModelObserver) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: IModelObserver) -> None:
        pass

    @abstractmethod
    def get_line(self, line_number: int) -> str:
        pass

    @abstractmethod
    def get_current_line(self) -> str:
        pass

    @abstractmethod
    def get_line_count(self) -> int:
        pass

    # Cursor operations
    @abstractmethod
    def get_cursor_position(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def set_cursor_position(self, line: int, column: int) -> None:
        pass

    @abstractmethod
    def move_cursor_to_line_start(self) -> None:
        pass

    @abstractmethod
    def move_cursor_to_line_end(self) -> None:
        pass

    @abstractmethod
    def move_cursor_word_forward(self) -> None:
        pass

    @abstractmethod
    def move_cursor_word_backward(self) -> None:
        pass

    @abstractmethod
    def insert_text(self, text: str) -> None:
        pass

    @abstractmethod
    def delete_char(self) -> None:
        pass

    @abstractmethod
    def delete_line(self) -> None:
        pass

    @abstractmethod
    def new_line(self) -> None:
        pass

    @abstractmethod
    def delete_word(self) -> None:
        pass

    @abstractmethod
    def replace_char(self, char: str) -> None:
        pass

    @abstractmethod
    def yank_line(self) -> None:
        pass

    @abstractmethod
    def yank_word(self) -> None:
        pass

    @abstractmethod
    def paste_after(self) -> None:
        pass

    @abstractmethod
    def load_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def show_help(self) -> None:
        pass

    @abstractmethod
    def save_file(self, filename: str = None) -> None:
        pass

    @abstractmethod
    def get_filename(self) -> str:
        pass

    @abstractmethod
    def is_modified(self) -> bool:
        pass

    @abstractmethod
    def get_mode(self) -> str:
        pass

    @abstractmethod
    def set_mode(self, mode: str) -> None:
        pass

    @abstractmethod
    def repeat_last_search(self, forward: bool = True) -> bool:
        pass

    @abstractmethod
    def delete_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def set_search_buffer(self, buffer: str) -> None:
        pass

    @abstractmethod
    def get_search_buffer(self) -> str:
        pass

    @abstractmethod
    def clear_search_buffer(self) -> None:
        pass

    @abstractmethod
    def set_tmp_filename(self, filename: str) -> None:
        pass

    @abstractmethod
    def get_tmp_filename(self,filename: str) -> str:
        pass
    @abstractmethod
    def _perform_search(self, text: str, forward: bool = True) -> None:
        pass
    
    @abstractmethod
    def set_last_search(self, text: str) ->None:
        pass

    @abstractmethod
    def set_last_search_forward(self, forward: bool) -> None:
        pass