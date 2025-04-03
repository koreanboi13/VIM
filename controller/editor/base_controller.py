from interfaces.i_controller import IController
from interfaces.i_model import IModel
from interfaces.i_view import IView
from interfaces.editor.i_input_handler import IInputHandler
from interfaces.editor.i_mode_handler import IModeHandler
from interfaces.editor.i_command_executor import ICommandExecutor
from interfaces.editor.i_movement_controller import IMovementController
from typing import Dict, Optional

class BaseController(IController):
    def __init__(self, 
                 model: IModel, 
                 view: IView,
                 input_handler: IInputHandler,
                 command_executor: ICommandExecutor):
        self._model = model
        self._view = view
        self._running = False
        self._input_handler = input_handler
        self._command_executor = command_executor
        self._mode_handlers: Dict[str, IModeHandler] = {}

    def register_mode_handler(self, mode: str, handler: IModeHandler) -> None:
        self._mode_handlers[mode] = handler

    def start(self) -> None:
        self._running = True
        self._view.init()
        self._model.add_observer(self._view)
        self._model.set_mode("NORMAL")

    def stop(self) -> None:
        self._running = False
        self._model.remove_observer(self._view)
        self._view.cleanup()

    def handle_input(self, key: str) -> bool:
        if not self._running:
            return False

        return self._input_handler.handle_input(key)
