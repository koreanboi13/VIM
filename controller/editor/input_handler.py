from interfaces.editor.i_input_handler import IInputHandler
from interfaces.i_model import IModel
from interfaces.editor.i_mode_handler import IModeHandler
from typing import Dict

class InputHandler(IInputHandler):
    def __init__(self, model: IModel, mode_handlers: Dict[str, IModeHandler]):
        self._model = model
        self._mode_handlers = mode_handlers

    def handle_input(self, key: str) -> bool:
        current_mode = self._model.get_mode()
        if current_mode in self._mode_handlers:
            return self._mode_handlers[current_mode].handle_mode(key)
        return False
