from interfaces.editor.i_mode_handler import IModeHandler
from interfaces.i_model import IModel
from interfaces.i_view import IView
from interfaces.editor.i_movement_controller import IMovementController
from interfaces.editor.i_command_executor import ICommandExecutor

class BaseModeHandler(IModeHandler):
    def __init__(self, 
                 model: IModel, 
                 view: IView,
                 command_executor: ICommandExecutor):
        self._model = model
        self._view = view
        self._command_executor = command_executor

    def handle_mode(self, key: str) -> bool:

        return False

    def enter_mode(self) -> None:
        pass

    def exit_mode(self) -> None:
        pass
