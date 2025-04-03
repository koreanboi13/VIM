from abc import ABC, abstractmethod
from typing import Optional
from interfaces.i_modelObs import IModelObserver

class IView(IModelObserver, ABC):
    @abstractmethod
    def init(self) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

    @abstractmethod
    def get_input(self) -> Optional[str]:
        pass

    @abstractmethod
    def set_command_buffer(self, buffer: str) -> None:
        pass

    @abstractmethod
    def set_search_buffer(self, buffer: str) -> None:
        pass

    @abstractmethod
    def display_error(self, message: str) -> None:
        pass

    @abstractmethod
    def display_info(self, message: str) -> None:
        pass
